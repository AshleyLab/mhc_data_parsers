#!/bin/sh
data_prefix=/oak/stanford/groups/euan/projects/mhc
#motionActivity & motionTracker tables 
python get_activity.py --tables $data_prefix/data/tables/cardiovascular-motionTracker-v1.tsv $data_prefix/data/tables/cardiovascular-motionActivityCollector-v1.tsv \
    --synapseCacheDir $data_prefix/mhc/data/synapseCache/ \
    --out_prefixes parsed_coreMotion \
    --data_types motion_tracker \
    --subjects $data_prefix/mhc/data/tables/subjects/motion.tracker/motion.subjects

