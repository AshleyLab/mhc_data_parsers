#NOTE: tested on python 3.6 w/ anaconda 3
#Author: annashch@stanford.edu
import numpy as np
import pandas as pd 
from datetime import datetime,timedelta,date
from dateutil.parser import parse
import pdb 
sample_gap_thresh=timedelta(minutes=15) 
min_allowed_time=date(2015,1,1)


#perform qc on healthkit entries to ensure they fall into humanly feasible ranges 
def qc_mt(data): 
    num_rows=data.shape[0]
    to_delete=[] 
    for row_index in range(num_rows): 
        cur_date=data[row_index]['startTime'].date()
        if (cur_date < min_allowed_time):
            to_delete.append(row_index)
    print(str(to_delete))
    data=np.delete(data,to_delete)        
    return data    
def qc_hk(datatype,value,startTime,endTime):
    #datatype=datatype.decode('utf-8') 
    if datatype not in ["HKQuantityTypeIdentifierDistanceWalk","HKQuantityTypeIdentifierStepCount"]:
        return True 
    if datatype=="HKQuantityTypeIdentifierDistanceWalk": 
        time_diff=(endTime-startTime).total_seconds()/60.0
        speed=value/time_diff
        if speed > 750: 
            print('BAD SPEED') 
            return False 
        else: 
            return True 
    if datatype=="HKQuantityTypeIdentifierStepCount": 
        time_diff=(endTime-startTime).total_seconds()/60.0 
        rate=value/time_diff 
        if rate >1000: 
            print("BAD RATE") 
            return False 
        else: 
            return True 

def get_activity_fractions_from_duration(duration_dict):
    fraction_dict=dict()
    for day in duration_dict:
        fraction_dict[day]=dict()
        total_duration=timedelta(minutes=0)
        for activity in duration_dict[day]:
            for blob in duration_dict[day][activity]: 
                total_duration+=abs(duration_dict[day][activity][blob])
        total_duration=total_duration.total_seconds()
        if total_duration > 0:
            for entry in duration_dict[day]:
                fraction_dict[day][entry]=dict() 
                for blob in duration_dict[day][entry]:
                    fraction_dict[day][entry][blob]=duration_dict[day][entry][blob].total_seconds()/total_duration
    return fraction_dict

def parse_motion_activity(file_path):
    cur_blob=file_path.split('/')[-2]
    duration_dict=dict()
    fraction_dict=dict()
    numentries=dict() 

    pandas_coumns=['startTime','activityType','confidence']
    try:
        data=pd.read_csv(file_path,
                         sep=',',
                         header='infer',
                         names=pandas_columns,
                         dtype={'value':np.float16},
                         parse_dates=['startTime'],
                         infer_datetime_format=True,
                         quotechar='"',
                         na_values=['value'],
                         error_bad_lines=False,
                        engine='c')
        first_col=pandas_columns[0]
        if(data.iloc[0][first_col]==first_col):
            data=data.drop([0])
    except: 
        print("there was a problem opening:"+str(file_path))
        return [duration_dict,fraction_dict,num_entries]
    #get the duration of each activity by day 
    first_row=0
    try:
        num_rows=data.shape[0]
        cur_time=data['startTime'][first_row]
        cur_day=data['startTime'][first_row].date() 
        cur_activity=data['activityType'][first_row]
        cur_confidence=data['confidence'][first_row] 
        while (cur_activity=="not available") and (first_row <(num_rows-1)) and (cur_confidence>0) :
            first_row+=1
            cur_time=data['startTime'][first_row]
            cur_day=data['startTime'][first_row].date() 
            cur_activity=data['activityType'][first_row]
            cur_confidence=data['confidence'][first_row] 
    except:
        return[duration_dict,fraction_dict,numentries]

    for row in range(first_row+1,num_rows):
        try:
            new_activity=data['activityType'][row]
            new_time=data['startTime'][row]
            new_day=data['startTime'][row].date()
            new_confidence=data['confidence'][row] 
            if (new_confidence < 1):
                continue 
            if(new_time-cur_time)<=sample_gap_thresh:
                if new_activity=="not available":
                    #carry forward from the previous activity 
                    new_activity=cur_activity
                duration=abs(new_time-cur_time)
                if cur_day not in duration_dict:
                    duration_dict[cur_day]=dict()
                    numentries[cur_day]=0
                if cur_activity not in duration_dict[cur_day]:
                    duration_dict[cur_day][cur_activity]=dict() 
                if cur_blob not in duration_dict[cur_day][cur_activity]: 
                    duration_dict[cur_day][cur_activity][cur_blob]=duration 
                else:
                    duration_dict[cur_day][cur_activity][cur_blob]+=duration
                numentries[cur_day]+=1  
            cur_activity=new_activity
            cur_time=new_time
            cur_day=new_day
        except:
            continue
    #get the activity fractions relative to total duration
    fraction_dict=get_activity_fractions_from_duration(duration_dict)
    return [duration_dict,fraction_dict,numentries]


def parse_healthkit_sleep(file_path): 
    cur_blob=file_path.split('/')[-2]
    tally_dict=dict() 
    try:
        data=pd.read_csv(file_path,
                         sep=',',
                         header='infer',
                         dtype = {'value': np.float16 },
                         parse_dates=['startTime'],
                         infer_datetime_format=True,
                         quotechar='"',
                         na_values=['value'],
                         error_bad_lines=False,
                         engine='c')
        first_col='startTime'
        if(data.iloc[0][first_col]==first_col):
          data= data.drop([0])
    except Exception as e: 
        print("There was a problem loading:"+str(file_path))
        return tally_dict
    #get the duration of each activity by day
    try:
        for index,row in data.iterrows():
            if row['startTime'] is not None:
                datatype=row['category value']
                source=row['source']
                sourceIdentifier=row['sourceIdentifier']
                source_tuple=tuple([source,sourceIdentifier])
                day=row['startTime'].date()
                value=row['value']
                if day not in tally_dict:
                    tally_dict[day]=dict()
                if datatype not in tally_dict[day]:
                    tally_dict[day][datatype]=dict()
                if source_tuple not in tally_dict[day][datatype]:
                    tally_dict[day][datatype][source_tuple]=dict() 
                if cur_blob not in tally_dict[day][datatype][source_tuple]:
                    tally_dict[day][datatype][source_tuple][cur_blob]=value
                else:
                    tally_dict[day][datatype][source_tuple][cur_blob]+=value
    except Exception as e:
        print("There was a problem parsing:"+str(file_path))
    return tally_dict

def parse_healthkit_workout(file_path): 
    cur_blob=file_path.split('/')[-2]
    tally_dict=dict() 
    try:
        data=pd.read_csv(file_path,
                         sep=',',
                         header='infer',
                         dtype = {'total distance':np.float16,
                                  'energy consumed':np.float16},
                         parse_dates=['startTime','endTime'],
                         infer_datetime_format=True,
                         quotechar='"',
                         na_values=['total distance'],
                         error_bad_lines=False,
                         engine='c')
        first_col='startTime'
        if(data.iloc[0][first_col]==first_col):
            data= data.drop([0])
    except Exception as e:
        print("There was a problem loading:"+str(file_path))
        return tally_dict
    #get the duration of each activity by day
    try:
        for index,row in data.iterrows():
            datatype=row['workoutType']
            source=row['source']
            sourceIdentifier=row['sourceIdentifier']
            source_tuple=tuple([source,sourceIdentifier])
            day=row['startTime'].date()
            value=row['energy consumed']
        if day not in tally_dict:
            tally_dict[day]=dict()
            if datatype not in tally_dict[day]:
                tally_dict[day][datatype]=dict()
            if source_tuple not in tally_dict[day][datatype]:
                tally_dict[day][datatype][source_tuple]=dict() 
            if cur_blob not in tally_dict[day][datatype][source_tuple]:
                tally_dict[day][datatype][source_tuple][cur_blob]=value
            else:
                tally_dict[day][datatype][source_tuple][cur_blob]+=value
    except Exception as e:
        print("There was a problem parsing:"+str(file_path))
    return tally_dict

def parse_healthkit_data(file_path):
    cur_blob=file_path.split('/')[-2]
    tally_dict=dict()
    try:
        data=pd.read_csv(file_path,
                         sep=',',
                         header='infer',
                         dtype = {'value': np.float16 },
                         parse_dates=['startTime','endTime'],
                         infer_datetime_format=True,
                         quotechar='"',
                         na_values=['value'],
                         error_bad_lines=False,
                         engine='c')
        if(data['startTime'][0]=='startTime'):
            data=data.drop([0])
    except:
        try:
            data=pd.read_csv(file_path,
                             sep=',',
                             header='infer',
                             dtype = {'value': np.float16 },
                             parse_dates=['datetime'],
                             infer_datetime_format=True,
                             quotechar='"',
                             na_values=['value'],
                             error_bad_lines=False,
                             engine='c')
            if(data['datetime'][0]=='datetime'): 
                data=data.drop([0])
        except Exception as e:
            print("There was a problem loading:"+str(file_path))
            return tally_dict
    #get the duration of each activity by day
    try:
        for index,row in data.iterrows():
            datatype=row['type']
            source=row['source']
            sourceIdentifier=row['sourceIdentifier']
            source_tuple=tuple([source,sourceIdentifier])
            value=row['value']
            if 'startTime' in data.columns:
                day=row['startTime'].date()
                qc_result=qc_hk(datatype,value,row['startTime'],row['endTime'])
            else: 
                day=row['datetime'].date()
                qc_result=True
            if qc_result==False: 
                continue 
            if day not in tally_dict:
                tally_dict[day]=dict()
            if datatype not in tally_dict[day]:
                tally_dict[day][datatype]=dict()
            if source_tuple not in tally_dict[day][datatype]:
                tally_dict[day][datatype][source_tuple]=dict() 
            if cur_blob not in tally_dict[day][datatype][source_tuple]:
                tally_dict[day][datatype][source_tuple][cur_blob]=value
            else:
                tally_dict[day][datatype][source_tuple][cur_blob]+=value
    except Exception as e:
        print("There was a problem importing:"+str(file_path))
    return tally_dict

if __name__=="__main__":
    #TESTS for sherlock
    import pdb
    base_dir="/oak/stanford/groups/euan/projects/mhc/data/synapseCache/"
    #health_kit_workout=parse_healthkit_workout(base_dir+"309/4661309/data.csv-5dc42cce-eab6-40c2-bd97-f51b78bb069d2034482356528994271.tmp") 
    health_kit_data=parse_healthkit_data(base_dir+"96/3082096/data.csv-5dbff042-7cf2-4d82-b627-ae1b406bfbb21795360669337449335.tmp")  #missing source, should error
    #health_kit_sleep=parse_healthkit_sleep(base_dir+"596/4478596/data.csv-40ce6eb1-c4d3-4dfb-8465-d25249b128307556370121217889486.tmp") 
    pdb.set_trace() 

    
