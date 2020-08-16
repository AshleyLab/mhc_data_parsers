#NOTE: tested on python 3
#Author: annashch@stanford.edu
import pdb 
import pytz
import numpy as np
import pandas as pd 
from datetime import datetime,timedelta,date
from dateutil.parser import parse
from synapse_openers import * 
from config import * 
from qc import * 


def parse_motion_activity(file_path,subject_blob_vals,subject_timestamp_blobs,cur_subject,aggregation_interval,healthkit_fields_to_use,get_median=False):
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

        cur_activity=data[activity_type_field].iloc[first_row]
        cur_confidence=data[confidence_field].iloc[first_row] 
        while ((cur_activity=="not available") or (cur_confidence < confidence_thresh)) and (first_row <(num_rows-1)):
            first_row+=1
            try:
                cur_time=data[start_time_field].iloc[first_row]
                if type(cur_time)==str: 
                    try:
                        cur_time=parse(cur_time) 
                    except:
                        continue
                row_string=','.join([str(i) for i in data.iloc[first_row]])
                if row_string in subject_timestamp_blobs[cur_subject]: 
                    subject_timestamp_blobs[cur_subject][row_string].append(cur_blob) 
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
            cur_aggregation_interval=cur_time.floor(freq=aggregation_interval)
            if cur_aggregation_interval.tzinfo is None: 
                cur_aggregation_interval=pytz.utc.localize(cur_aggregation_interval)
            new_activity=data[activity_type_field].iloc[row]
            new_time=data[start_time_field].iloc[row]
            if type(new_time)==str: 
                new_time=parse(new_time)
            #check for a duplicate blob entry
            row_string=','.join([str(i) for i in data.iloc[row]])
            if row_string in subject_timestamp_blobs[cur_subject]: 
                subject_timestamp_blobs[cur_subject][row_string].append(cur_blob)
                continue 
            else: 
                subject_timestamp_blobs[cur_subject][row_string]=[cur_blob] 
            
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
                    if get_median is True: 
                        subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['Median']=[duration]
                else: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['Minutes']+=duration
                    subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['N']+=1
                    subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['Blobs'].add(cur_blob)
                    if get_median is True: 
                        subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['Median'].append(duration)
                    
            cur_activity=new_activity
            cur_time=new_time
        except Exception as e:
            continue
    return subject_blob_vals,subject_timestamp_blobs


def parse_healthkit_sleep(file_path, subject_blob_vals, subject_timestamp_blobs,cur_subject,aggregation_interval,healthkit_fields_to_use,get_median=False):
    cur_blob, data=open_healthkit_sleep(file_path)
    if data is None: 
        return subject_blob_vals,subject_timestamp_blobs        
    #get the duration of each activity by day
    try:
        for index,row in data.iterrows():
            if row['startTime'] is not None:

                datatype=row['category value']
                source=row['source']
                sourceIdentifier=row['sourceIdentifier']
                source_tuple=tuple([source,sourceIdentifier])
                cur_time=row['startTime']
                if type(cur_time)==str: 
                    try:
                        cur_time=parse(cur_time) 
                    except: 
                        continue
                cur_aggregation_interval=cur_time.floor(freq=aggregation_interval)
                if cur_aggregation_interval.tzinfo is None: 
                    cur_aggregation_interval=pytz.utc.localize(cur_aggregation_interval)

                value=row['value']
                
                row_string=','.join([str(i) for i in row])
                if row_string in subject_timestamp_blobs[cur_subject]: 
                    subject_timestamp_blobs[cur_subject][row_string].append(cur_blob)
                    continue 
                else: 
                    subject_timestamp_blobs[cur_subject][row_string]=[cur_blob] 

                if cur_aggregation_interval not in subject_blob_vals[cur_subject]: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval]={}

                if datatype not in subject_blob_vals[cur_subject][cur_aggregation_interval]: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]={} 

                if source_tuple not in subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]={'Min':value,'Max':value,'N':1,'Sum':value,'Blobs':set([cur_blob])} 
                    if get_median is True: 
                        subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Median']=[value]
                else: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['N']+=1
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Sum']+=value
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Blobs'].add(cur_blob)
    
                    if value < subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Min']:
                        subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Min']=value
                    if value > subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Max']:
                        subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Max']=value
                    if get_median is True: 
                        subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Median'].append(value)

    except Exception as e:
        raise
        print("There was a problem parsing:"+str(file_path))
    return subject_blob_vals, subject_timestamp_blobs 

def parse_healthkit_workout(file_path,subject_blob_vals,subject_timestamp_blobs,cur_subject,aggregation_interval,healthkit_fields_to_use,get_median=False): 
    cur_blob,data=open_healthkit_workout(file_path) 
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
                try:
                    cur_time=parse(cur_time) 
                except: 
                    continue
            #check for a duplicate blob entry
            row_string=','.join([str(i) for i in row])
            if row_string in subject_timestamp_blobs[cur_subject]: 
                subject_timestamp_blobs[cur_subject][row_string].append(cur_blob)
                continue 
            else: 
                subject_timestamp_blobs[cur_subject][row_string]=[cur_blob] 

            datatype=row['workoutType']
            source=row['source']
            sourceIdentifier=row['sourceIdentifier']
            source_tuple=tuple([source,sourceIdentifier])
            energy=row['energy consumed']
            distance=row['total distance'] 
            cur_aggregation_interval=cur_time.floor(freq=aggregation_interval)
            if cur_aggregation_interval.tzinfo is None: 
                cur_aggregation_interval=pytz.utc.localize(cur_aggregation_interval)
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

def parse_healthkit_data(file_path,subject_blob_vals,subject_timestamp_blobs,cur_subject,aggregation_interval,healthkit_fields_to_use,get_median=False):
    cur_blob,data=open_healthkit_data(file_path) 
    if data is None: 
        return subject_blob_vals,subject_timestamp_blobs 
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
            row_string=','.join([str(i) for i in row])
            if row_string in subject_timestamp_blobs[cur_subject]: 
                subject_timestamp_blobs[cur_subject][row_string].append(cur_blob)
                continue 
            else: 
                subject_timestamp_blobs[cur_subject][row_string]=[cur_blob] 
            
            if(type(cur_time)==str): 
                try:
                    cur_time=parse(cur_time)
                except: 
                    continue
            cur_aggregation_interval=cur_time.floor(freq=aggregation_interval)
            if cur_aggregation_interval.tzinfo is None: 
                cur_aggregation_interval=pytz.utc.localize(cur_aggregation_interval)

            if cur_aggregation_interval not in subject_blob_vals[cur_subject]: 
                subject_blob_vals[cur_subject][cur_aggregation_interval]={}
            if datatype not in subject_blob_vals[cur_subject][cur_aggregation_interval]: 
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]={} 
            if source_tuple not in subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]: 
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]={'Min':value,'Max':value,'Sum':value,'N':1,'Blobs':set([cur_blob])}
                if get_median is True: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Median']=[value]

            else: 
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['N']+=1
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Sum']+=value
                subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Blobs'].add(cur_blob)
                if value < subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Min']:
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Min']=value
                if value > subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Max']:
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Max']=value
                if get_median is True: 
                    subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Median'].append(value)

    except Exception as e:
        raise
        print("There was a problem importing:"+str(file_path))
    return subject_blob_vals,subject_timestamp_blobs 

if __name__=="__main__":
    #TESTS for sherlock
    import pdb
    #TEST THIS:

    #totest="/oak/stanford/groups/euan/projects/mhc/data/synapseCache/462/53682462/aX5zucSVNrnoPhxVJ-Pli3_7-data.csv"
    #totest="/oak/stanford/groups/euan/projects/mhc/data/synapseCache/283/54263283/ckTBHR5A0PNmOj2qKZn1QqQP-data.csv" #data with stepcount
    #totest="/oak/stanford/groups/euan/projects/mhc/data/synapseCache/484/52726484/MGYsiBzDt3rp1gvn4UxFaubL-data.csv" #coremotion from phone 
    totest="/oak/stanford/groups/euan/projects/mhc/data/synapseCache/415/53280415/QEqIDu77MmNXmvN0op3b5_iy-data.csv" #workout 
    healthCode="2c7b48bb-fd41-447e-b189-984dd43f4048"
    #health_kit_data,subject_timestamp_blobs=parse_healthkit_data(totest,{healthCode:{}},{healthCode:{}},healthCode,10,["HKQuantityTypeIdentifierStepCount"])
    #motion_data,motion_timestamp_blobs=parse_motion_activity(totest,{healthCode:{}},{healthCode:{}},healthCode,10,None)
    workout_data,workout_timestamp_blobs=parse_healthkit_workout(totest,{healthCode:{}},{healthCode:{}},healthCode,'1D','all')
    pdb.set_trace() 


