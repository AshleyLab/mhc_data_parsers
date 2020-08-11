#!/bin/bash
#DataCollector PeakVO2
data_prefix=/oak/stanford/groups/euan/projects/mhc

python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
    -synapseCacheDir $data_prefix/data/synapseCache/ \
    -out_prefixes out/parsed_HealthKitData.PeakVO2.10min.$1 \
    -data_types health_kit_data_collector \
    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
    --health_kit_fields_to_use HKQuantityTypeIdentifierVO2Max \
    --aggregation_interval 10


python get_activity.py -tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitDataCollector-v1.tsv \
    -synapseCacheDir $data_prefix/data/synapseCache/ \
    -out_prefixes out/parsed_HealthKitData.PeakVO2.1440min.$1 \
    -data_types health_kit_data_collector \
   --subjects $data_prefix/data/tables/2.3.2/subjects/hk_data_collector/x$1 \
    --health_kit_fields_to_use HKQuantityTypeIdentifierVO2Max \
    --aggregation_interval 1440
