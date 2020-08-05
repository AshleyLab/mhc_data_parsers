#!/bin/sh

#10 minute, steps 
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.StepCount.10min. \
    --first 0 \
    --last 139 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.StepCount.10min.txt

#10 minute, steps, duplicates 
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.StepCount.10min. \
    --first 0 \
    --last 139 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.StepCount.10min.duplicate.timestamps.txt \
    --suffix .duplicate.timestamps 

