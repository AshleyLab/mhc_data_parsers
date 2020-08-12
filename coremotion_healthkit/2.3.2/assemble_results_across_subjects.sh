
#10 minute, steps 
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.StepCount.10min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.StepCount.10min.txt

#10 minute, steps, duplicates 
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.StepCount.10min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.StepCount.10min.duplicate.timestamps.txt \
    --suffix .duplicate.timestamps 

#1440 minute, steps 
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.StepCount.1440min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.StepCount.1440min.txt

#1440 minute, steps, duplicates
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.StepCount.1440min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.StepCount.1440min.duplicate.timestamps.txt \
    --suffix .duplicate.timestamps

#10 minute, distance 
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.Distance.10min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.Distance.10min.txt

#10 minute, distance, duplicates 
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.Distance.10min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.Distance.10min.duplicate.timestamps.txt \
    --suffix .duplicate.timestamps

#1440 minute, distance 
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.Distance.1440min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.Distance.1440min.txt

#1440 minute, distance, duplicates 
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.Distance.1440min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.Distance.1440min.duplicate.timestamps.txt \
    --suffix .duplicate.timestamps

#10 minute, heart rate
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.HeartRate.10min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.HeartRate.10min.txt

#10 minute, heart rate, duplicates
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.HeartRate.10min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.HeartRate.10min.duplicate.timestamps.txt \
    --suffix .duplicate.timestamps

#1440 minute, heart rate  
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.HeartRate.1440min. \
       --first 0 \
       --last 152 \
       --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.HeartRate.1440min.txt

#1440 minute, heart rate, duplicates
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.HeartRate.1440min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.HeartRate.1440min.duplicate.timestamps.txt \
    --suffix .duplicate.timestamps

#1440 minute, motion activity phone
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_motionActivity.1440min. \
    --first 0 \
    --last 125 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_motionActivity.1440min.txt

#1440 minute, motion activity phone, duplicates
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_motionActivity.1440min. \
    --first 0 \
    --last 125 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_motionActivity.1440min.duplicate.timestamps.txt \
    --suffix .duplicate.timestamps

#1440 minute, motion activity watch
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_motionActivity_watch.1440min. \
    --first 0 \
    --last 20 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_motionActivity_watch.1440min.txt

#1440 minute, motion activity watch, duplicates
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_motionActivity_watch.1440min. \
    --first 0 \
    --last 20 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_motionActivity_watch.1440min.duplicate.timestamps.txt \
    --suffix .duplicate.timestamps

#1440 minute, HealthKit Workout 
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitWorkout.1440min. \
    --first 0 \
    --last 71 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitWorkout.1440min.txt

#1440 minute, HealthKit Workout, duplicates
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitWorkout.1440min. \
    --first 0 \
    --last 71 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitWorkout.1440min.duplicate.timestamps.txt \
    --suffix .duplicate.timestamps

#1440 minute, HealthKit Sleep 
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitSleep.1440min. \
    --first 0 \
    --last 72 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitSleep.1440min.txt

#1440 minute, HealthKit Sleep, duplicates
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitSleep.1440min. \
    --first 0 \
    --last 72 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitSleep.1440min.duplicate.timestamps.txt \
    --suffix .duplicate.timestamps

#10 minute, RHR
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.RestingHR.10min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.RestingHR.10min.txt

#1440 minute, RHR 
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.RestingHR.1440min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.RestingHR.1440min.txt

#10 minutes, HRVariability
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.HRVariability.10min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.HRVariability.10min.txt

#1440 minutes, HRVariabiltiy
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.HRVariability.1440min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.HRVariability.1440min.txt

#1 week, HRVariability
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.HRVariability.1week. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.HRVariability.1week.txt

#10 minutes, WalkingHR
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.WalkingHR.10min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.WalkingHR.10min.txt

#1440 minutes, WalkingHR
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.WalkingHR.1440min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.WalkingHR.1440min.txt


#10 minutes, BPDiastolic
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.BPDiastolic.10min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.BPDiastolic.10min.txt

#1440 minutes, BPDiastolic
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.BPDiastolic.1440min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.BPDiastolic.1440min.txt


#10 minutes, BPSystolic
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.BPSystolic.10min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.BPSystolic.10min.txt

#1440 minutes, BPSystolic
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.BPSystolic.1440min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.BPSystolic.1440min.txt


#10 minutes, PeakVO2
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.PeakVO2.10min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.PeakVO2.10min.txt

#1440 minutes, PeakVO2
python assemble_results_across_subjects.py --prefix /oak/stanford/groups/euan/users/annashch/mhc_data_parsers/coremotion_healthkit/2.3.2/out/parsed_HealthKitData.PeakVO2.1440min. \
    --first 0 \
    --last 152 \
    --outf /oak/stanford/groups/euan/projects/mhc/data/timeseries_2.3.2/parsed_HealthKitData.PeakVO2.1440min.txt
