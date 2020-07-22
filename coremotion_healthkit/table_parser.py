#parses data tables
import pandas as pd 
from table_loader import *
from synapse_parser import *
from datetime import datetime,timedelta
import pdb
from os import listdir
from os.path import isfile, join
import warnings
warnings.filterwarnings("ignore")

synapse_parser_choices={"motion_tracker":parse_motion_activity,
                      "health_kit_data_collector":parse_healthkit_data,
                      "health_kit_sleep_collector":parse_healthkit_sleep,
                      "health_kit_workout_collector":parse_healthkit_workout}

def get_synapse_cache_entry(synapseCacheDir,blob_name):
    parent_dir=blob_name[-3::].lstrip('0')
    if parent_dir=="":
        parent_dir="0" 
    mypath=synapseCacheDir+parent_dir+"/"+blob_name
    try:
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        onlyfiles=[f for f in onlyfiles if "data.csv" in f]
        #first, check if there are any filtered files. 
        priority=[f for f in onlyfiles if f.endswith('filtered')]
        if len(priority)>0: 
            return mypath+'/'+priority[0] 
        priority=[f for f in onlyfiles if ".csv" in f]
        if len(priority)>0: 
            return mypath+'/'+priority[0] 
        #only return a single file in case there are copies (i.e. multiple data pulls of the same file seem to create copies) 
        return mypath+'/'+onlyfiles[0]        
    except: 
        return None

def remove_null_blobs(data_table,column_name): 
    '''
    remove rows with null values for a given column
    '''
    print(data_table.shape)
    data_table.dropna(axis=0,how='any',subset=[column_name],inplace=True) 
    data_table=data_table[data_table[column_name]!="NA"]
    data_table=data_table[data_table[column_name]!="None"]
    data_table=data_table[pd.notnull(data_table[column_name])]
    print(data_table.shape) 
    return data_table 

def parse_table(table_path,synapseCacheDir,data_type,subjects,aggregation_interval,healthkit_fields_to_use):
    data_table=load_table(table_path)
    print("loaded summary data table") 

    #filter to subjects to keep 
    if subjects!="all": 
        subjects=open(subjects,'r').read().strip().split('\n')
        data_table=data_table[data_table['healthCode'].isin(subjects)]
        print("filtered data table to specified subjects") 

    blob_col='data.csv'
    data_table=remove_null_blobs(data_table,blob_col)
    print("removed null blobs from data table") 

    #keep track of activity metrics 
    subject_blob_vals={}

    #keep track of timestamps that occur in multiple blobs for a given subject 
    subject_timestamp_blobs={} 
    total_rows=data_table.shape[0]
    cur_row=0 
    for index,row in data_table.iterrows():
        cur_row+=1
        if cur_row%100==0:
            print(str(cur_row)+"/"+str(total_rows))
        cur_subject=row['healthCode']
        if cur_subject not in subject_timestamp_blobs: 
            subject_timestamp_blobs[cur_subject]={} 
        if cur_subject not in subject_blob_vals:
            subject_blob_vals[cur_subject]={} 

        blob_name=row[blob_col]
        synapseCacheFile=get_synapse_cache_entry(synapseCacheDir,blob_name)
        subject_blob_vals,subject_timestamp_blobs=synapse_parser_choices[data_type](synapseCacheFile,
                                                                                    subject_blob_vals,
                                                                                    subject_timestamp_blobs,
                                                                                    cur_subject,
                                                                                    aggregation_interval,
                                                                                    healthkit_fields_to_use)
    return subject_blob_vals, subject_timestamp_blobs 

if __name__=="__main__":
    #TESTS 
    synapseCacheDir="/oak/stanford/groups/euan/projects/mhc/data/synapseCache/"
    subjects="/oak/stanford/groups/euan/projects/mhc/data/tables/subjects/hk/hk.workout"    
    #workouts
    #workout_table_path="/oak/stanford/groups/euan/projects/mhc/data/tables/cardiovascular-HealthKitWorkoutCollector-v1.tsv"
    #workouts=parse_healthkit_workout_collector(workout_table_path,synapseCacheDir,subjects)     
    #data
    data_table_path="/oak/stanford/groups/euan/projects/mhc/data/tables/cardiovascular-HealthKitDataCollector-v1.tsv"
    data=parse_healthkit_workout_collector(data_table_path,synapseCacheDir,subjects)     
    #sleep
    sleep_table_path="/oak/stanford/groups/euan/projects/mhc/data/tables/cardiovascular-HealthKitSleepCollector-v1.tsv"
    sleep=parse_healthkit_workout_collector(sleep_table_path,synapseCacheDir,subjects)     
    pdb.set_trace()
    

