#!/bin/sh
data_prefix=/oak/stanford/groups/euan/projects/mhc


#DataCollector Steps 1440 minute interval 
python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
    -synapseCacheDir $data_prefix/data/synapseCache/ \
    -out_prefixes out/parsed_HealthKitData.StepCount.1440min.$1 \
    -data_types health_kit_data_collector \
    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
    --health_kit_fields_to_use HKQuantityTypeIdentifierStepCount \
    --aggregation_interval 1440

echo "done with steps, 1440 mins"

#DataCollector Distance 10 minute interval
python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
    -synapseCacheDir $data_prefix/data/synapseCache/ \
    -out_prefixes out/parsed_HealthKitData.Distance.10min.$1 \
    -data_types health_kit_data_collector \
    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
    --health_kit_fields_to_use HKQuantityTypeIdentifierDistanceWalkingRunning \
    --aggregation_interval 10

echo "done with distance, 10 mins"

#DataCollector Steps 1440 minute interval 
python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
    -synapseCacheDir $data_prefix/data/synapseCache/ \
    -out_prefixes out/parsed_HealthKitData.Distance.1440min.$1 \
    -data_types health_kit_data_collector \
    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
    --health_kit_fields_to_use HKQuantityTypeIdentifierDistanceWalkingRunning \
    --aggregation_interval 1440

echo "done with distance, 1440 mins"

#DataCollector HeartRate 10 minute interval
python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
    -synapseCacheDir $data_prefix/data/synapseCache/ \
    -out_prefixes out/parsed_HealthKitData.HeartRate.10min.$1 \
    -data_types health_kit_data_collector \
    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
    --health_kit_fields_to_use HKQuantityTypeIdentifierHeartRate \
    --aggregation_interval 10

echo "done with HR, 10 mins" 

#DataCollector HeartRate 1440 minute interval 
python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
    -synapseCacheDir $data_prefix/data/synapseCache/ \
    -out_prefixes out/parsed_HealthKitData.HeartRate.1440min.$1 \
    -data_types health_kit_data_collector \
    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
    --health_kit_fields_to_use HKQuantityTypeIdentifierHeartRate \
    --aggregation_interval 1440

echo "done with HR, 1440 mins" 
