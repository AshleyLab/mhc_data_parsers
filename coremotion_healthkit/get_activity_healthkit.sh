#!/bin/sh
data_prefix=/oak/stanford/groups/euan/projects/mhc
#DataCollector 
python get_activity.py --tables $data_prefix/mhc/data/tables/cardiovascular-HealthKitDataCollector-v1.tsv \
    --synapseCacheDir $data_prefix/mhc/data/synapseCache/ \
    --out_prefixes parsed_HealthKitData \
    --data_types health_kit_data_collector \
    --subjects $data_prefix/mhc/data/tables/subjects/hk.datacollector

#SleepCollector
python get_activity.py --tables $data_prefix/data/tables/cardiovascular-HealthKitSleepCollector-v1.tsv \
    --synapseCacheDir $data_prefix/mhc/data/synapseCache/ \
    --out_prefixes HealthKitSleep \
    --data_types health_kit_sleep_collector \
    --subjects $data_prefix/mhc/data/tables/subjects/hk.sleep


#Workout Collector 
python get_activity.py --tables $data_prefix/mhc/data/tables/cardiovascular-HealthKitWorkoutCollector-v1.tsv \
    --synapseCacheDir $data_prefix/mhc/data/synapseCache/ \
    --out_prefixes HealthKitWorkout \
    --data_types health_kit_workout_collector \
    --subjects $data_prefix/mhc/data/tables/subjects/hk.workout
