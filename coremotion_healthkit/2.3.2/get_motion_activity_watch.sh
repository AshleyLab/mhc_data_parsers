#!/bin/sh
data_prefix=/oak/stanford/groups/euan/projects/mhc
#motionActivity table
python get_activity.py -tables $data_prefix/data/tables/2.3.2/watchMotionActivityCollector-v1.tsv \
    -synapseCacheDir $data_prefix/data/synapseCache/ \
    -out_prefixes out/parsed_motionActivity_watch.1440min.$1 \
    -data_types motion_tracker \
    --subjects $data_prefix/data/tables/2.3.2/subjects/motion_watch/x$1 \
    --aggregation_interval '1D'

