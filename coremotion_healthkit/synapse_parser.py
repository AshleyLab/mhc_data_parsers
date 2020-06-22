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
        if time_diff==0: 
            return True
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
    duration_dict=dict()
    fraction_dict=dict()
    num_entries=dict() 
    parseAs=None
    try:
        cur_blob=file_path.split('/')[-2]
    except: 
        return [duration_dict,fraction_dict,num_entries]
    try:
        pandas_columns=['startTime','activityType','confidence']
        data=pd.read_csv(file_path,
                         sep=',',
                         header='infer',
                         dtype={'value':np.float16},
                         parse_dates=['startTime'],
                         infer_datetime_format=True,
                         quotechar='"',
                         error_bad_lines=False,
                         index_col=False,
                         engine='python')        
        
        first_col=pandas_columns[0]
        if(data.iloc[0][first_col]==first_col):
            data=data.drop([0])
        parse_as='motion_activity'
    except :
        try:
            pandas_columns=["dateAndTime","activityTypeName","activityTypeValue","confidenceName","confidenceRaw","confidencePercent"]
            data=pd.read_csv(file_path,
                             sep=',',
                             header='infer',
                             parse_dates=['dateAndTime'],
                             infer_datetime_format=True,
                             quotechar='"',
                             error_bad_lines=False,
                             index_col=False,
                             engine='python')
            first_col=pandas_columns[0]
            if(data.iloc[0][first_col]==first_col):
                data=data.drop([0])
            parse_as='motion_tracker'
        except:
            try:                
                data=pd.read_csv(file_path,
                                 sep=',',
                                 header=None,
                                 names=['startTime','activityType','confidence'],
                                 parse_dates=['startTime'],
                                 infer_datetime_format=True,
                                 quotechar='"',
                                 error_bad_lines=False,
                                 index_col=False,
                                 engine='python')
                parse_as='motion_activity'
            except:
                print("there was a problem opening:"+str(file_path))
                return [duration_dict,fraction_dict,num_entries]
    #get the duration of each activity by day 
    first_row=0
    try:        
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
        cur_day=cur_time.date()

        while (cur_activity=="not available") and (first_row <(num_rows-1)) and (cur_confidence>0) :
            first_row+=1
            try:
                cur_time=data[start_time_field].iloc[first_row]
                if type(cur_time)==str: 
                    cur_time=parse(cur_time) 
                cur_day=cur_time.date()
                cur_activity=data[activity_type_field].iloc[first_row]
                cur_confidence=data[confidence_field].iloc[first_row] 
            except: 
                continue 
    except Exception as e:
        return[duration_dict,fraction_dict,num_entries]

    for row in range(first_row+1,num_rows):
        try:
            new_activity=data[activity_type_field].iloc[row]
            new_time=data[start_time_field].iloc[row]
            if type(new_time)==str: 
                new_time=parse(new_time) 
            new_day=new_time.date()
            new_confidence=data[confidence_field].iloc[row] 
            if (new_confidence < 1):
                continue 
            if(new_time-cur_time)<=sample_gap_thresh:
                if new_activity=="not available":
                    #carry forward from the previous activity 
                    new_activity=cur_activity
                duration=abs(new_time-cur_time)
                if cur_day not in duration_dict:
                    duration_dict[cur_day]=dict()
                    num_entries[cur_day]=0
                if cur_activity not in duration_dict[cur_day]:
                    duration_dict[cur_day][cur_activity]=dict() 
                if cur_blob not in duration_dict[cur_day][cur_activity]: 
                    duration_dict[cur_day][cur_activity][cur_blob]=duration 
                else:
                    duration_dict[cur_day][cur_activity][cur_blob]+=duration
                num_entries[cur_day]+=1  
            cur_activity=new_activity
            cur_time=new_time
            cur_day=new_day
        except Exception as e:
            continue
    #get the activity fractions relative to total duration
    fraction_dict=get_activity_fractions_from_duration(duration_dict)
    return [duration_dict,fraction_dict,num_entries]


def parse_healthkit_sleep(file_path):
    tally_dict=dict() 
    try:
        cur_blob=file_path.split('/')[-2]
    except: 
        return tally_dict
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
                         index_col=False,
                         engine='python')
        first_col='startTime'
        if(data.iloc[0][first_col]==first_col):
          data= data.drop([0])
    except:
        try:
            data=pd.read_csv(file_path,
                             sep=',',
                             names=['startTime','type','category value','value','unit','source','sourceIdentifier','appVersion'],
                             header=None,
                             dtype = {'value': np.float16 },
                             parse_dates=['startTime'],
                             infer_datetime_format=True,
                             quotechar='"',
                             na_values=['value'],
                             error_bad_lines=False,
                             index_col=False,
                             engine='python')
        except:
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
    tally_dict=dict() 
    try:
        cur_blob=file_path.split('/')[-2]
    except: 
        return tally_dict
    try:
        data=pd.read_csv(file_path,
                         sep=',',
                         header='infer',
                         dtype = {'total distance':np.float16,
                                  'energy consumed':np.float16},
                         parse_dates=['startTime','endTime'],
                         infer_datetime_format=True,
                         na_values=['total distance'],
                         error_bad_lines=False,
                         index_col=False,
                         quotechar='"',
                         usecols=[0,1,2,3,4,5,6,7,8,9],
                         engine='python')
        first_col='startTime'
        if(data.iloc[0][first_col]==first_col):
            data= data.drop([0])
    except:
        try:
            data=pd.read_csv(file_path,
                 sep=',',
                 header='infer',
                 dtype = {'total distance':np.float16,
                          'energy consumed':np.float16},
                 parse_dates=['startTime','endTime'],
                 infer_datetime_format=True,
                 na_values=['total distance'],
                 error_bad_lines=False,
                 index_col=False,
                 quotechar='|',
                 usecols=[0,1,2,3,4,5,6,7,8,9],
                 engine='python')
            first_col='startTime'
            if(data.iloc[0][first_col]==first_col):
                data= data.drop([0])
        except:
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
    tally_dict=dict()
    try:
        cur_blob=file_path.split('/')[-2]
    except: 
        return tally_dict
    #print(str(file_path))
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
                         index_col=False,
                         engine='python')
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
                             usecols=list(range(0,6)),
                             na_values=['value'],
                             error_bad_lines=False,
                             index_col=False,
                             engine='python')
            if(data['datetime'][0]=='datetime'): 
                data=data.drop([0])
        except:
            try:
                data=pd.read_csv(file_path,
                                 sep=',',
                                 header=None,
                                 names=['startTime','endTime','type','value','unit','source','sourceIdentifier','appVersion'],
                                 dtype = {'value': np.float16 },
                                 parse_dates=['startTime','endTime'],
                                 infer_datetime_format=True,
                                 quotechar='"',
                                 na_values=['value'],
                                 error_bad_lines=False,
                                 index_col=False,
                                 engine='python')
            except: 
                print("There was a problem loading:"+str(file_path))
                return tally_dict
    #get the duration of each activity by day
    try:
        for index,row in data.iterrows():
            datatype=row['type']
            source=row['source']
            #sourceIdentifier=row['sourceIdentifier']
            #source_tuple=tuple([source,sourceIdentifier])
            source_tuple=tuple([source])#,sourceIdentifier])
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
        print(row) 
        print("There was a problem importing:"+str(file_path))
    return tally_dict

if __name__=="__main__":
    #TESTS for sherlock
    import pdb
    #TEST THIS:
    #/oak/stanford/groups/euan/projects/mhc/data/synapseCache/462/53682462/aX5zucSVNrnoPhxVJ-Pli3_7-data.csv

    base_dir="/oak/stanford/groups/euan/projects/mhc/data/synapseCache/"
    #health_kit_workout=parse_healthkit_workout("/oak/stanford/groups/euan/projects/mhc/data/synapseCache/519/53353519/ZiaHJYutH7oFmuldBBWovdc0-data.csv") 
    #health_kit_data=parse_healthkit_data(base_dir+"464/53479464/Re4XGq-MVInIYhpgNeVNPXFU-data.csv")  #missing source, should error
    health_kit_sleep=parse_healthkit_sleep("/oak/stanford/groups/euan/projects/mhc/data/synapseCache/206/54023206/UA85W-3sTuKDYu7Nf5RcE2_U-data.csv") 
    #cm=parse_motion_activity("/oak/stanford/groups/euan/projects/mhc/data/synapseCache/591/53720591/BN93l3Ttc71mwMUryZ5kJWA6-data.csv")
    #cm=parse_motion_activity("/oak/stanford/groups/euan/projects/mhc/data/synapseCache/583/46695583/27a1ef5f-c581-4867-8f72-551af1d40c7d-data.csv")
    #health_kit_sleep=parse_healthkit_sleep("/oak/stanford/groups/euan/projects/mhc/data/synapseCache/305/7841305/data-8978e7f6-7b47-4a08-b7a5-f45f34598e09.csv")

    pdb.set_trace() 


    
