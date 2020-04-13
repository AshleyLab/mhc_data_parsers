#!/bin/sh
data_prefix=/oak/stanford/groups/euan/projects/mhc

#SleepCollector
python get_activity.py --tables $data_prefix/data/tables/cardiovascular-HealthKitSleepCollector-v1.tsv \
    --synapseCacheDir $data_prefix/data/synapseCache/ \
    --out_prefixes out/parsed_HealthKitSleep.$1 \
    --data_types health_kit_sleep_collector \
    --subjects $data_prefix/data/tables/subjects/hk/hk_sleep/x$1

