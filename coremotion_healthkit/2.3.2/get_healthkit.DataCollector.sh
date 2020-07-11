#!/bin/sh
data_prefix=/oak/stanford/groups/euan/projects/mhc
#DataCollector 
python get_activity.py --tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
    --synapseCacheDir $data_prefix/data/synapseCache/ \
    --out_prefixes out/parsed_HealthKitData.$1 \
    --data_types health_kit_data_collector \
    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1

