#!/bin/sh
data_prefix=/oak/stanford/groups/euan/projects/mhc

#SleepCollector
python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitSleepCollector-v1.tsv \
    -synapseCacheDir $data_prefix/data/synapseCache/ \
    -out_prefixes out/parsed_HealthKitSleep.1440min.$1 \
    -data_types health_kit_sleep_collector \
    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_sleep/x$1 \
    --aggregation_interval 1440


