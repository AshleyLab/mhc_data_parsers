#!/bin/sh
data_prefix=/oak/stanford/groups/euan/projects/mhc
#motionActivity table
python get_activity.py --tables $data_prefix/data/tables/cardiovascular-motionActivityCollector-v1.tsv \
    --synapseCacheDir $data_prefix/data/synapseCache/ \
    --out_prefixes out/parsed_motionActivity.$1 \
    --data_types motion_tracker \
    --subjects $data_prefix/data/tables/subjects/motion.activity/motion_activity/x$1
