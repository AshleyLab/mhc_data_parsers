#!/usr/bin/env python

import sys
import os
import glob
import logging

import numpy as np
import pandas as pd
import datetime
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

plt.style.use('seaborn-white')


def main():
    """run script
    """
    # hard paths - NOTE: CHANGE IF DIFFERENT SERVER/FILES
    PARSER_DIR="/home/groups/khavari/users/dskim89/git/mhc_data_parsers"
    MHC_DIR="/oak/stanford/groups/euan/projects/mhc/data"
    SYNAPSE_CACHE="{}/synapseCache/".format(MHC_DIR)

    # conversions
    tablename_to_datatype = {
        "HealthKitDataCollector": "health_kit_data_collector"}

    # args
    healthcode_id = sys.argv[1]
    xml_zip = sys.argv[2]
    if len(sys.argv) >= 4:
        WORK_DIR = sys.argv[3]
    else:
        WORK_DIR = "."

    # logging
    logging.basicConfig(
        filename="run.{}.log".format(healthcode_id),
        level=logging.INFO,
        format="%(message)s")

    # -----------------------------
    # open xml and load data
    # -----------------------------

    # unzip
    xml_dir = "{}/apple_health_export.{}".format(WORK_DIR, healthcode_id)
    if not os.path.isdir(xml_dir):
        unzip = "unzip {} -d {}".format(xml_zip, WORK_DIR)
        print(unzip)
        os.system(unzip)
        os.system("mv {}/apple_health_export {}".format(WORK_DIR, xml_dir))

    # parse
    os.system("mkdir -p {}/xml.{}".format(WORK_DIR, healthcode_id))
    xml_out_prefix = "{0}/xml.{1}/xml.{1}".format(WORK_DIR, healthcode_id)
    xml_files = glob.glob("{}*".format(xml_out_prefix))
    if len(xml_files) == 0:
        parse_cmd = (
            "python {}/xml/parse_xml_export.py "
            "--xmlfile {}/export.xml "
            "--out_prefix {}").format(
                PARSER_DIR,
                xml_dir,
                xml_out_prefix)
        print(parse_cmd)
        os.system(parse_cmd)
    xml_files = glob.glob("{}*".format(xml_out_prefix))

    # -----------------------------
    # now load from synapse cache
    # -----------------------------
    
    # make simplified sample file
    healthcodes_file = "{}/healthcodes_to_extract.tmp.txt".format(WORK_DIR)
    if not os.path.isfile(healthcodes_file):
        with open(healthcodes_file, "w") as fp:
            fp.write(healthcode_id)

    # make simplified table
    # TODO make user input correct table file?
    print("WARNING: using test subjects table - adjust in script as needed!")
    #orig_table_file = "{}/tables/test_subjects/cardiovascular-HealthKitDataCollector-v1.tsv".format(MHC_DIR)
    #orig_table_file = "{}/tables/test_subjects/cardiovascular-motionActivityCollector-v1.tsv".format(MHC_DIR)
    orig_table_file = "{}/tables/cardiovascular-HealthKitDataCollector-v1.tsv".format(MHC_DIR)
    table_file = "{}/table_to_synapse.filt.{}.txt".format(WORK_DIR, healthcode_id)
    if not os.path.isfile(table_file):
        filt_cmd = "cat {} | awk 'NR == 1 || /{}/' > {}".format(
            orig_table_file, healthcode_id, table_file)
        print(filt_cmd)
        os.system(filt_cmd)
        
    # parse
    # NOTE: the parse seems to aggregate by day?
    synapse_out_file = "{}/synapse.{}.{}".format(
        WORK_DIR, healthcode_id, os.path.basename(orig_table_file))
    if not os.path.isfile(synapse_out_file):
    #if True:
        parse_cmd = (
            "python {}/coremotion_healthkit/get_activity.py "
            "--tables {} "
            "--data_types {} "
            "--synapseCacheDir {} "
            "--subjects {} "
            "--out_prefixes {} ").format(
                PARSER_DIR,
                table_file,
                "health_kit_data_collector", # TODO modularize this
                SYNAPSE_CACHE,
                healthcodes_file,
                synapse_out_file)
        print(parse_cmd)
        os.system(parse_cmd)

    # -----------------------------
    # now compare
    # -----------------------------

    # first start with synapse and pull metrics from there
    synapse_data = pd.read_csv(
        synapse_out_file, sep="\t",
        parse_dates=["Date"],
        infer_datetime_format=True)
    metrics = sorted(synapse_data["Metric"].drop_duplicates().values.tolist())
    logging.info("{} metrics found for user {} in synapseCache".format(
        len(metrics), healthcode_id))

    # set up plot area. make sure to clear fig each time new plot
    plt.figure()

    # for each metric, compare xml file to synapse
    total_xml_metrics_seen = 0
    for metric in metrics:
        for xml_file in xml_files:
            if metric in xml_file:
                logging.info("{}".format(metric))

                # debug
                #if "HKQuantityTypeIdentifierStepCount" not in metric:
                #    continue
                    
                # =======================
                # XML
                # =======================
                # process xml
                # NOTE: no qc checks here, unlike Anna parsers
                xml_data = pd.read_csv(
                    xml_file, sep="\t", 
                    parse_dates=["@startDate", "@endDate"],
                    infer_datetime_format=True)

                # QC: try to match Anna's QC check on startTime and endTime
                #if False:
                if metric == "HKQuantityTypeIdentifierStepCount": 
                    # NOTE this doesn't seem to do much
                    print(metric)
                    print(xml_data.shape)
                    xml_data["time_diff"] = (xml_data["@endDate"] - xml_data["@startDate"])
                    xml_data["time_diff"] = xml_data["time_diff"].dt.total_seconds() / 60.0
                    xml_data["rate"] = xml_data["@value"] / xml_data["time_diff"]
                    # if rate < 1000 OR time_diff == 0 (ie rate is inf), keep
                    xml_data = xml_data.replace([np.inf, -np.inf], 0)                    
                    xml_data = xml_data[xml_data["rate"] <= 1000]
                    print(xml_data.shape)
                if metric == "HKQuantityTypeIdentifierDistanceWalk": 
                    # NOTE this doesn't seem to do much
                    print(metric)
                    print(xml_data.shape)
                    xml_data["time_diff"] = (xml_data["@endDate"] - xml_data["@startDate"])
                    xml_data["time_diff"] = xml_data["time_diff"].dt.total_seconds() / 60.0
                    xml_data["rate"] = xml_data["@value"] / xml_data["time_diff"]
                    # if rate < 1000 OR time_diff == 0 (ie rate is inf), keep
                    xml_data = xml_data.replace([np.inf, -np.inf], 0)                    
                    xml_data = xml_data[xml_data["rate"] <= 750]
                    print(xml_data.shape)
                    

                
                # clean up xml data
                xml_data = xml_data[["@type", "@sourceName", "@sourceVersion", "@device", "@startDate", "@value"]]

                # fix timezone
                # NOTE: this may change from user to user
                print("WARNING: timezone adjustment (check manually right now)")
                xml_data["@startDate"] = xml_data["@startDate"].dt.tz_convert('US/Pacific')
                xml_data["Date"] = xml_data["@startDate"].dt.date


                try:
                    # get hardware device
                    xml_data["hardware"] = xml_data["@device"].str.split(",", expand=True)[4]
                    xml_data["hardware"] = xml_data["hardware"].fillna("Other")
                    xml_data.loc[xml_data["hardware"] == ""] = "Other"
                except AttributeError:
                    xml_data["hardware"] = xml_data["@device"].fillna("Other")
                    xml_data.loc[xml_data["hardware"] == ""] = "Other"

                # plot by device
                if False:
                    plot_file = "{}/xml.{}.{}.DEVICE.png".format(WORK_DIR, healthcode_id, metric)
                    print(plot_file)
                    ax = sns.scatterplot(x="Date", y="@value", hue="hardware", data=xml_data, s=5, linewidth=0)
                    ax.set_xlim(xml_data['Date'].min(), xml_data['Date'].max())
                    ax.xaxis.set_major_formatter(DateFormatter("%Y"))
                    ax.xaxis.set_major_locator(mdates.YearLocator(1))
                    ax.xaxis.grid(True) # Show the vertical gridlines
                    ax.set_title("{}\nuser {}".format(metric, healthcode_id))
                    plt.savefig(plot_file, height=2, width=2)
                    plt.clf()
                    
                # plot by source version
                if False:
                    plot_file = "{}/xml.{}.{}.VERSION.png".format(WORK_DIR, healthcode_id, metric)
                    print(plot_file)
                    ax = sns.scatterplot(x="Date", y="@value", hue="@sourceVersion", data=xml_data, s=5, linewidth=0)
                    ax.set_xlim(xml_data['Date'].min(), xml_data['Date'].max())
                    ax.xaxis.set_major_formatter(DateFormatter("%Y"))
                    ax.xaxis.set_major_locator(mdates.YearLocator(1))
                    ax.xaxis.grid(True) # Show the vertical gridlines
                    ax.set_title("{}\nuser {}".format(metric, healthcode_id))
                    plt.savefig(plot_file, height=2, width=2)
                    plt.clf()

                # aggregate: by date, with version info
                xml_data["@sourceVersion"] = xml_data["@sourceVersion"].astype(str)
                version_agg = pd.DataFrame(xml_data.groupby(["Date"])["@sourceVersion"].agg("unique"))
                version_agg["@sourceVersion"] = version_agg["@sourceVersion"].apply(sorted).apply(",".join)

                # aggregate: by date, the values
                values_agg = pd.DataFrame(xml_data.groupby(["Date"])["@value"].sum())
                values_agg.columns = ["xml"]

                # aggregate: by date, the device
                devices_agg = pd.DataFrame(xml_data.groupby(["Date"])["hardware"].agg("unique"))
                devices_agg["hardware"] = devices_agg["hardware"].apply(sorted).apply(",".join)

                # merge all aggregated
                xml_data = values_agg.merge(version_agg, left_index=True, right_index=True)
                xml_data = xml_data.merge(devices_agg, left_index=True, right_index=True)

                # =======================
                # synapse
                # =======================
                # synapse: filter for metric and sources
                synapse_data_filt = synapse_data[synapse_data["Metric"] == metric]
                synapse_data_filt = synapse_data_filt.sort_values(["Date"])
                synapse_data_filt = synapse_data_filt[
                    ["Date", "Value", "Source", "SourceBlobs"]].set_index("Date")
                synapse_data_filt.columns = ["synapse", "Source", "SourceBlobs"]
                synapse_data_filt["SourceBlobs"] = synapse_data_filt["SourceBlobs"].str.split(",")
                synapse_data_filt["Source"] = synapse_data_filt["Source"].apply(eval)
                source_tmp = pd.DataFrame(synapse_data_filt['Source'].tolist(), index=synapse_data_filt.index)
                synapse_data_filt["device"] = source_tmp[0]

                # TEST: filter out for just iphone
                #synapse_data_filt = synapse_data_filt[synapse_data_filt["device"].str.contains("iphone", case=False)]
                #print(synapse_data_filt)
                

                # =======================
                # merge
                # =======================
                compare_data = xml_data.merge(
                    synapse_data_filt, 
                    how="outer", left_index=True, right_index=True)
                compare_data = compare_data.fillna(0)

                # cleanup
                compare_data["@sourceVersion"] = compare_data["@sourceVersion"].astype(str)
                compare_data["hardware"] = compare_data["hardware"].astype(str)

                # ignore dates when the app was updated
                compare_data = compare_data[~compare_data["@sourceVersion"].str.contains(",")]

                # debug
                #print(compare_data)
                #print(compare_data.columns)
                #print(compare_data["@sourceVersion"].values)

                compare_file = "{}/compare.{}.{}.txt.gz".format(WORK_DIR, healthcode_id, metric)
                compare_data.to_csv(compare_file, sep="\t", compression="gzip")

                # first, see num entries
                logging.info("    {} entries in synapse; {} entries in xml".format(
                    synapse_data_filt.shape[0], xml_data.shape[0]))

                # plots: by value, color by various measures: none, software, hardware
                plot_file = "{}/compare.{}.{}.vals.png".format(WORK_DIR, healthcode_id, metric)
                print(plot_file)
                ax = sns.scatterplot(x="xml", y="synapse", data=compare_data, s=5, linewidth=0)
                ax.set_title("{}\nuser {}".format(metric, healthcode_id))
                plt.savefig(plot_file, height=2, width=2)
                plt.clf()

                if True:
                    plot_file = "{}/compare.{}.{}.vals.BY_VERSION.png".format(WORK_DIR, healthcode_id, metric)
                    print(plot_file)
                    ax = sns.scatterplot(x="xml", y="synapse", hue="@sourceVersion", data=compare_data, s=5, linewidth=0, palette="deep")
                    ax.set_title("{}\nuser {}".format(metric, healthcode_id))
                    plt.savefig(plot_file, height=2, width=2)
                    plt.clf()

                    plot_file = "{}/compare.{}.{}.vals.BY_DEVICE.png".format(WORK_DIR, healthcode_id, metric)
                    print(plot_file)
                    ax = sns.scatterplot(x="xml", y="synapse", hue="hardware", data=compare_data, s=5, linewidth=0)
                    ax.set_title("{}\nuser {}".format(metric, healthcode_id))
                    plt.savefig(plot_file, height=2, width=2)
                    plt.clf()

                # plot by date
                if False:
                    compare_data_melt = compare_data.reset_index().melt(id_vars="Date")
                    plot_file = "{}/compare.{}.{}.BY_DATE.png".format(WORK_DIR, healthcode_id, metric)
                    print(plot_file)
                    ax = sns.scatterplot(x="Date", y="value", hue="variable", data=compare_data_melt)
                    ax.set(xticklabels=[])
                    ax.set_title("{}\nuser {}".format(metric, healthcode_id))
                    plt.savefig(plot_file, height=2, width=2)
                    plt.clf()

                # set up for diff plots
                compare_data["present"] = ["Present" if val != 0 else "Missing.S" for val in compare_data["synapse"].values]
                compare_data["diff.xml-synapse"] = compare_data["xml"] - compare_data["synapse"]
                compare_data = compare_data.reset_index()

                # plots: chronology, color by various measures: none, software, hardware
                plot_file = "{}/compare.{}.{}.chronological.DIFF.png".format(WORK_DIR, healthcode_id, metric)
                print(plot_file)
                ax = sns.scatterplot(x="Date", y="diff.xml-synapse", hue="present", data=compare_data, s=5, linewidth=0)
                ax.set_xlim(compare_data['Date'].min(), compare_data['Date'].max())
                ax.xaxis.grid(True) # Show the vertical gridlines
                ax.xaxis.set_major_formatter(DateFormatter("%Y")) # set up major tick by year
                ax.xaxis.set_major_locator(mdates.YearLocator(1)) # increment every 1 year
                ax.set_title("{}\nuser {}".format(metric, healthcode_id))
                plt.savefig(plot_file, height=2, width=2)
                plt.clf()

                if True:
                    plot_file = "{}/compare.{}.{}.chronological.DIFF.BY_VERSION.png".format(WORK_DIR, healthcode_id, metric)
                    print(plot_file)
                    ax = sns.scatterplot(x="Date", y="diff.xml-synapse", hue="@sourceVersion", data=compare_data, s=5, linewidth=0, palette="deep")
                    ax.set_xlim(compare_data['Date'].min(), compare_data['Date'].max())
                    ax.xaxis.grid(True) # Show the vertical gridlines
                    ax.xaxis.set_major_formatter(DateFormatter("%Y")) # set up major tick by year
                    ax.xaxis.set_major_locator(mdates.YearLocator(1)) # increment every 1 year
                    ax.set_title("{}\nuser {}".format(metric, healthcode_id))
                    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.) # legend outside fig
                    plt.savefig(plot_file, height=2, width=3, bbox_inches="tight")
                    plt.clf()

                    plot_file = "{}/compare.{}.{}.chronological.DIFF.BY_DEVICE.png".format(WORK_DIR, healthcode_id, metric)
                    print(plot_file)
                    ax = sns.scatterplot(x="Date", y="diff.xml-synapse", hue="hardware", data=compare_data, s=5, linewidth=0)
                    ax.set_xlim(compare_data['Date'].min(), compare_data['Date'].max())
                    ax.xaxis.grid(True) # Show the vertical gridlines
                    ax.xaxis.set_major_formatter(DateFormatter("%Y")) # set up major tick by year
                    ax.xaxis.set_major_locator(mdates.YearLocator(1)) # increment every 1 year
                    ax.set_title("{}\nuser {}".format(metric, healthcode_id))
                    plt.savefig(plot_file, height=2, width=2)
                    plt.clf()

                    # plot by source blob?
                    source_data = compare_data.explode("SourceBlobs")
                    source_data["SourceBlobs"] = source_data["SourceBlobs"].astype(str)
                    plot_file = "{}/compare.{}.{}.BY_SOURCE_BLOB.png".format(WORK_DIR, healthcode_id, metric)
                    ax = sns.scatterplot(
                        x="SourceBlobs", y="diff.xml-synapse", hue="present", data=source_data, s=5, linewidth=0)
                    ax.set(xticklabels=[])
                    ax.set_title("{}\nuser {}".format(metric, healthcode_id))
                    plt.savefig(plot_file, height=2, width=2)
                    plt.clf()

                # iterate
                total_xml_metrics_seen += 1
                
    logging.info("{} xml metrics; {} seen in synapse".format(
        len(xml_files), total_xml_metrics_seen))

    # clean up
    os.system("rm {}/*tmp.txt".format(WORK_DIR))

    return


main()
