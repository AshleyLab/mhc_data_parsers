#!/bin/bash
#DataCollector HeartRate 10 minute interval 
data_prefix=/oak/stanford/groups/euan/projects/mhc

#python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
#    -synapseCacheDir $data_prefix/data/synapseCache/ \
#    -out_prefixes out/parsed_HealthKitData.RestingHR.10min.$1 \
#    -data_types health_kit_data_collector \
#    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
#    --health_kit_fields_to_use HKQuantityTypeIdentifierRestingHeartRate \
#    --aggregation_interval 10


#python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
#    -synapseCacheDir $data_prefix/data/synapseCache/ \
#    -out_prefixes out/parsed_HealthKitData.RestingHR.1440min.$1 \
#    -data_types health_kit_data_collector \
#   --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
#    --health_kit_fields_to_use HKQuantityTypeIdentifierRestingHeartRate \
#    --aggregation_interval 1440



#python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
#    -synapseCacheDir $data_prefix/data/synapseCache/ \
#    -out_prefixes out/parsed_HealthKitData.HRVariability.10min.$1 \
#    -data_types health_kit_data_collector \
#    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
#    --health_kit_fields_to_use HKQuantityTypeIdentifierHeartRateVariabilitySDNN \
#    --aggregation_interval 10


#python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
#    -synapseCacheDir $data_prefix/data/synapseCache/ \
#    -out_prefixes out/parsed_HealthKitData.HRVariability.1440min.$1 \
#    -data_types health_kit_data_collector \
#   --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
#    --health_kit_fields_to_use HKQuantityTypeIdentifierHeartRateVariabilitySDNN \
#    --aggregation_interval 1440

#Weekly medians 
python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
    -synapseCacheDir $data_prefix/data/synapseCache/ \
    -out_prefixes out/parsed_HealthKitData.HRVariability.1week.$1 \
    -data_types health_kit_data_collector \
    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
    --health_kit_fields_to_use HKQuantityTypeIdentifierHeartRateVariabilitySDNN \
    --aggregation_interval 10080 \
    --get_median


#python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
#    -synapseCacheDir $data_prefix/data/synapseCache/ \
#    -out_prefixes out/parsed_HealthKitData.WalkingHR.10min.$1 \
#    -data_types health_kit_data_collector \
#    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
#    --health_kit_fields_to_use HKQuantityTypeIdentifierWalkingHeartRateAverage \
#    --aggregation_interval 10


#python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
#    -synapseCacheDir $data_prefix/data/synapseCache/ \
#    -out_prefixes out/parsed_HealthKitData.WalkingHR.1440min.$1 \
#    -data_types health_kit_data_collector \
#   --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
#    --health_kit_fields_to_use HKQuantityTypeIdentifierWalkingHeartRateAverage \
#    --aggregation_interval 1440


