#!/bin/sh
data_prefix=/oak/stanford/groups/euan/projects/mhc

#Workout Collector 
python get_activity.py --tables $data_prefix/data/tables/2.3.2/cardiovascular-HealthKitWorkoutCollector-v1.tsv \
    --synapseCacheDir $data_prefix/data/synapseCache/ \
    --out_prefixes out/parsed_HealthKitWorkout.$1 \
    --data_types health_kit_workout_collector \
    --subjects $data_prefix/data/tables/2.3.2/subjects/hk_workout/x$1

