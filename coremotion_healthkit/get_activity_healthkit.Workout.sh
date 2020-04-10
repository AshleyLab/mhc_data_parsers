#!/bin/sh
data_prefix=/oak/stanford/groups/euan/projects/mhc


#Workout Collector 
python get_activity.py --tables $data_prefix/data/tables/cardiovascular-HealthKitWorkoutCollector-v1.tsv \
    --synapseCacheDir $data_prefix/data/synapseCache/ \
    --out_prefixes HealthKitWorkout \
    --data_types health_kit_workout_collector \
    --subjects $data_prefix/data/tables/subjects/hk/hk.workout
