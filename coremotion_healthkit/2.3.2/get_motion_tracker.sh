#!/bin/sh
data_prefix=/oak/stanford/groups/euan/projects/mhc
#motionTracker table 
python get_activity.py --tables $data_prefix/data/tables/cardiovascular-motionTracker-v1.tsv \
    --synapseCacheDir $data_prefix/data/synapseCache/ \
    --out_prefixes out/parsed_motionTracker.$1 \
    --data_types motion_tracker \
    --subjects $data_prefix/data/tables/subjects/motion.tracker/motion_tracker/x$1

