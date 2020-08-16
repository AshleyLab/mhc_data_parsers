#!/bin/bash
#DataCollector HeartRate 10 minute interval 
data_prefix=/oak/stanford/groups/euan/projects/mhc

#10 min
python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
    -synapseCacheDir $data_prefix/data/synapseCache/ \
    -out_prefixes out/parsed_HealthKitData.RHR.10min.$1 \
    -data_types health_kit_data_collector \
    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
    --health_kit_fields_to_use HKQuantityTypeIdentifierRestingHeartRate \
    --aggregation_interval '10min'

#1 day
python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
    -synapseCacheDir $data_prefix/data/synapseCache/ \
    -out_prefixes out/parsed_HealthKitData.RHR.1440min.$1 \
    -data_types health_kit_data_collector \
   --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
    --health_kit_fields_to_use HKQuantityTypeIdentifierRestingHeartRate \
    --aggregation_interval '1D'


