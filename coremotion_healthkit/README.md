# Scripts to aggregate core motion and healthkit activity 

## Data 
Tables are on oak: 
`/oak/stanford/groups/euan/projects/mhc/data/tables` 

Timeseries data from HealthKit and Core Motion is in the synapseCache folder on oak: 
`/oak/stanford/groups/euan/projects/mhc/data/synapseCache`


to map from a table row to the correpsonding synapseCache entry, identify the 'data.csv' column: 
```
ROW_ID	ROW_VERSION	recordId	appVersion	phoneInfo	uploadDate	healthCode	externalId	dataGroups	createdOn	createdOnTimeZone
	userSharingScope	validationErrors	substudyMemberships	dayInStudy	data.csv	rawData
1	0	0	f7e3d221-5109-4b38-9873-02976b7787b2	NA	NA	2015-04-14	a63a89b7-952a-417b-a3f0-98b89756bf51	NA	NA	2015-04-14 00:22:
49	NA	NA	NA	NA	NA	3065654	NA
```
the data.csv entry above is 3065654. 
The corresponding synapseCache entry would be in the folder with the last 3 digits of the blob id (654) , and then the folder with the full blob id: 

```
[annashch@sh02-02n32 /oak/stanford/groups/euan/projects/mhc/data/synapseCache/654/3065654]$ pwd 
/oak/stanford/groups/euan/projects/mhc/data/synapseCache/654/3065654
```

## Processed data (parser outputs): 

`/oak/stanford/groups/euan/projects/mhc/data/timeseries_allversions`

## Scripts to parse HealthKit and Core Motion datasets 

### HealthKit:

* get_healthkit.DataCollector.sh
* get_healthkit.Sleep.sh
* get_healthkit.Workout.sh

### Core Motion (2 tables, "activity" & "tracker") 
* get_motion_activity.sh
* get_motion_tracker.sh

## scripts to assemble across different subsets of subjects 
* assemble_results_across_subjects.sh

## Sbatch scripts for data processing on sherlock 

### HealthKit
* sbatch_get_hk_data.sh
* sbatch_get_hk_sleep.sh
* sbatch_get_hk_workout.sh

### Core Motion 
* sbatch_get_motion_activity.sh 
* sbatch_get_motion_tracker.sh
