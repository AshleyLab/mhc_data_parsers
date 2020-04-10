#!/bin/sh
data_prefix=/oak/stanford/groups/euan/projects/mhc
#DataCollector 
python get_activity.py --tables $data_prefix/data/tables/cardiovascular-HealthKitDataCollector-v1.tsv \
    --synapseCacheDir $data_prefix/data/synapseCache/ \
    --out_prefixes parsed_HealthKitData \
    --data_types health_kit_data_collector \
    --subjects $data_prefix/data/tables/subjects/hk/hk.datacollector
