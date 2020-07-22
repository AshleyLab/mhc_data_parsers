#NOTE: tested on python 3
#Author: annashch@stanford.edu
import numpy as np
import pandas as pd 
from datetime import datetime,timedelta,date
from dateutil.parser import parse
from synapse_openers import * 
from config import * 
from qc import * 


def parse_motion_activity(file_path,subject_blob_vals,subject_timestamp_blobs,cur_subject,aggregation_interval,healthkit_fields_to_use):
    parseAs=None
    cur_blob,data,parse_as=open_motion_activity_synapse(file_path) 
    if data is None: 
        return subject_blob_vals,subject_timestamp_blobs
    #get the duration of each activity by aggregation_interval
    first_row=0
    try:        
        #get the first row with valid activity entry 
        num_rows=data.shape[0]
        if parse_as=="motion_activity":
            start_time_field='startTime'
            activity_type_field='activityType' 
            confidence_field='confidence'
        else: 
            start_time_field='dateAndTime'
            activity_type_field='activityTypeName'
            confidence_field='confidenceRaw'

        cur_time=data[start_time_field].iloc[first_row]
        if(type(cur_time)==str): 
            cur_time=parse(cur_time)
        
        cur_activity=data[activity_type_field].iloc[first_row]
        cur_confidence=data[confidence_field].iloc[first_row] 
        while (cur_activity=="not available") and (first_row <(num_rows-1)) and (cur_confidence>0) :
            first_row+=1
            try:
                cur_time=data[start_time_field].iloc[first_row]
                if type(cur_time)==str: 
                    cur_time=parse(cur_time) 

                if cur_time in subject_timestamp_blobs[subject]: 
                    subject_timestamp_blobs[subject][cur_time].append(cur_blob) 
                    continue 

                cur_activity=data[activity_type_field].iloc[first_row]
                cur_confidence=data[confidence_field].iloc[first_row] 
            except: 
                continue 
    except Exception as e:
        return subject_blob_vals,subject_timestamp_blobs
    #parse through all remaining rows 
    for row in range(first_row+1,num_rows):
        try:
            cur_aggregation_interval=datetime.fromtimestamp((cur_time.timestamp()//(aggregation_interval*60))*(aggregation_interval*60))
            
            new_activity=data[activity_type_field].iloc[row]
            new_time=data[start_time_field].iloc[row]
            if type(new_time)==str: 
                new_time=parse(new_time) 

            if new_time in subject_timestamp_blobs[cur_subject]: 
                subject_timestamp_blobs[cur_subject][new_time].append(cur_blob) 
                continue 
            else: 
                subject_timestamp_blobs[cur_subject][new_time]=[cur_blob]                        
            
            new_confidence=data[confidence_field].iloc[row] 
            if (new_confidence < confidence_thresh):
                continue 
            if(new_time-cur_time)<=sample_gap_thresh:
                if new_activity=="not available":
                    #carry forward from the previous activity 
                    new_activity=cur_activity
                duration=abs(new_time-cur_time)
                if cur_aggregation_interval not in subject_blob_vals[cur_subject]: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval]={'TotalMinutes':duration}
                else: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval]['TotalMinutes']+=duration
                if cur_activity not in subject_blob_vals[cur_subject][cur_aggregation_interval]:
                    subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]={"Minutes":duration,"N":1,'Blobs':set([cur_blob])}
                else: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['Minutes']+=duration
                    subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['N']+=1
                    subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['Blobs'].add(cur_blob)
                    
            cur_activity=new_activity
            cur_time=new_time
        except Exception as e:
            continue
    return subject_blob_vals,subject_timestamp_blobs


def parse_healthkit_sleep(file_path, subject_blob_vals, subject_timestamp_blobs,cur_subject,aggregation_interval,healthkit_fields_to_use):
    tally_dict=dict() 
    cur_blob,data=open_healthkit_sleep(file_path)
    if data is None: 
        return tally_dict,subject_timestamp_blobs        
    
    #get the duration of each activity by day
    try:
        for index,row in data.iterrows():
            if row['startTime'] is not None:
                cur_time=row['startTime']
                if type(cur_time)==str: 
                    cur_time=parse(cur_time) 
                if cur_time not in subject_timestamp_blobs[cur_suject]: 
                    subject_timestamp_blobs[cur_subject][cur_time]=[cur_blob]
                else:
                    subject_timestamp_blobs[cur_subject][cur_time].append(cur_blob)
                    continue 
                datatype=row['category value']
                source=row['source']
                sourceIdentifier=row['sourceIdentifier']
                source_tuple=tuple([source,sourceIdentifier])
                cur_aggregation_interval=(cur_time.timestamp()//(aggregation_interval*60))*(aggregation_interval*60).gmtime() 
                value=row['value']
                
                if cur_aggregation_interval not in subject_blob_vals[cur_subject]: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval]={}
                if datatype not in subject_blob_vals[cur_subject][cur_aggregation_interval]: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]={} 
                if source_tuple not in subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]={'Min':value,'Max':value,'N':1,'Sum':value,'Blobs':set([cur_blob])} 
                else: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['N']+=1
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Sum']+=value
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Blobs'].add(cur_blob)
                    
                    if value < subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Min']:
                        subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Min']=value
                    if value > subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Max']:
                        subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Max']=value
    except Exception as e:
        raise
        print("There was a problem parsing:"+str(file_path))
    return subject_timestamp_blobs, tally_dict

def parse_healthkit_workout(file_path,subject_blob_vals,subject_timestamp_blobs,cur_subject,aggregation_interval,healthkit_fields_to_use): 
    cur_blob,data=open_healthkit_workout(filepath) 
    if data is None: 
        return subject_blob_vals, subject_timestamp_blobs 

    #filter to just fields of interest 
    if healthkit_fields_to_use!="all": 
        data=data[data['workoutType'].isin(healthkit_fields_to_use)]

    #get the duration & energy of each workout/device source combination
    try:
        for index,row in data.iterrows():
            cur_time=row['startTime'] 
            if type(cur_time)==str:
                cur_time=parse(cur_time) 
            #check for a duplicate blob entry for this timestamp
            if cur_time in subject_timestamp_blobs[cur_subject]: 
                subject_timestamp_blobs[cur_subject][cur_time].append(cur_blob)
                continue 
            else: 
                subject_timestamp_blobs[cur_subject][cur_time]=[cur_blob] 

            datatype=row['workoutType']
            source=row['source']
            sourceIdentifier=row['sourceIdentifier']
            source_tuple=tuple([source,sourceIdentifier])
            energy=row['energy consumed']
            distance=row['total distance'] 
            cur_aggregation_interval=(cur_time.timestamp()//(aggregation_interval*60))*(aggregation_interval*60).gmtime() 
                
            if cur_aggregation_interval not in subject_blob_vals[cur_subject]: 
                subject_blob_vals[cur_subject][cur_aggregation_interval]={}
            if datatype not in subject_blob_vals[cur_subject][cur_aggregation_interval]: 
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]={} 
            if source_tuple not in subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]: 
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]={'Distance':distance,'Energy':energy,'N':1,'Blobs':set([cur_blob])}
            else: 
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['N']+=1
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Distance']+=distance
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Energy']+=energy
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Blobs'].add(cur_blob)
    except Exception as e:
        print("There was a problem parsing:"+str(file_path))
    return subject_blob_vals,subject_timestamp_blobs 

def parse_healthkit_data(file_path,subject_blob_vals,subject_timestamp_blobs,cur_subject,aggregation_interval,healthkit_fields_to_use):
    cur_blob,data=open_healthkit_data(file_path) 
    if data is None: 
        return tally_dict,subject_timestamp_blobs 
    if healthkit_fields_to_use is not 'all': 
        data=data[data['type'].isin(healthkit_fields_to_use)]
    #get the duration of each activity by day
    try:
        for index,row in data.iterrows():
            datatype=row['type']
            source=row['source']
            source_tuple=tuple([source])
            value=row['value']
            
            #check for feasible values 
            if 'startTime' in data.columns:
                cur_time=row['startTime']
                qc_result=qc_hk(datatype,value,cur_time,row['endTime'])
            else: 
                cur_time=row['datetime']
                qc_result=True
            if qc_result==False: 
                continue 

            #check for a duplicate blob entry
            if type(cur_time)==str: 
                cur_time=parse(cur_time) 
            if cur_time in subject_timestamp_blobs[cur_subject]: 
                subject_timestamp_blobs[cur_subject][cur_time].append(cur_blob) 
                continue 
            else: 
                subject_timestamp_blobs[cur_subject][cur_time]=[cur_blob]

            cur_aggregation_interval=datetime.fromtimestamp((cur_time.timestamp()//(aggregation_interval*60))*(aggregation_interval*60))
            if cur_aggregation_interval not in subject_blob_vals[cur_subject]: 
                subject_blob_vals[cur_subject][cur_aggregation_interval]={}
            if datatype not in subject_blob_vals[cur_subject][cur_aggregation_interval]: 
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]={} 
            if source_tuple not in subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]: 
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]={'Min':value,'Max':value,'Sum':value,'N':1,'Blobs':set([cur_blob])}
            else: 
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['N']+=1
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Sum']+=value
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Blobs'].add(cur_blob)
                if value < subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Min']:
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Min']=value
                if value > subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Max']:
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Max']=value
    except Exception as e:
        print("There was a problem importing:"+str(file_path))
    return subject_blob_vals,subject_timestamp_blobs 

if __name__=="__main__":
    #TESTS for sherlock
    import pdb
    #TEST THIS:
    totest="/oak/stanford/groups/euan/projects/mhc/data/synapseCache/462/53682462/aX5zucSVNrnoPhxVJ-Pli3_7-data.csv"

    base_dir="/oak/stanford/groups/euan/projects/mhc/data/synapseCache/"
    health_kit_data,subject_timestamp_blobs=parse_healthkit_data(totest,{},"None")
    #health_kit_workout=parse_healthkit_workout("/oak/stanford/groups/euan/projects/mhc/data/synapseCache/519/53353519/ZiaHJYutH7oFmuldBBWovdc0-data.csv") 
    #health_kit_data=parse_healthkit_data(base_dir+"464/53479464/Re4XGq-MVInIYhpgNeVNPXFU-data.csv",{},'None')  #missing source, should error
    #health_kit_sleep=parse_healthkit_sleep("/oak/stanford/groups/euan/projects/mhc/data/synapseCache/206/54023206/UA85W-3sTuKDYu7Nf5RcE2_U-data.csv") 
    #cm=parse_motion_activity("/oak/stanford/groups/euan/projects/mhc/data/synapseCache/591/53720591/BN93l3Ttc71mwMUryZ5kJWA6-data.csv")
    #cm=parse_motion_activity("/oak/stanford/groups/euan/projects/mhc/data/synapseCache/583/46695583/27a1ef5f-c581-4867-8f72-551af1d40c7d-data.csv")
    #health_kit_sleep=parse_healthkit_sleep("/oak/stanford/groups/euan/projects/mhc/data/synapseCache/305/7841305/data-8978e7f6-7b47-4a08-b7a5-f45f34598e09.csv")

    pdb.set_trace() 


    
