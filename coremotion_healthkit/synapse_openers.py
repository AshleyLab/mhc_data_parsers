import pandas as pd 
import numpy as np 

def open_healthkit_data(file_path):
    try:
        cur_blob=file_path.split('/')[-2]
    except: 
        return None,None
    try:
        data=pd.read_csv(file_path,
                         sep=',',
                         header='infer',
                         dtype = {'value': np.float64 },
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
                             dtype = {'value': np.float64 },
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
                                 dtype = {'value': np.float64 },
                                 parse_dates=['startTime','endTime'],
                                 infer_datetime_format=True,
                                 quotechar='"',
                                 na_values=['value'],
                                 error_bad_lines=False,
                                 index_col=False,
                                 engine='python')
            except:
                print("There was a problem loading:"+str(file_path))
                return None,None
    return cur_blob,data

def open_healthkit_workout(file_path): 
    try:
        cur_blob=file_path.split('/')[-2]
    except: 
        return None,None
    try:
        data=pd.read_csv(file_path,
                         sep=',',
                         header='infer',
                         dtype = {'total distance':np.float64,
                                  'energy consumed':np.float64},
                         parse_dates=['startTime','endTime'],
                         infer_datetime_format=True,
                         na_values=['total distance'],
                         error_bad_lines=False,
                         index_col=False,
                         quotechar='"',
                         usecols=[0,1,2,3,4,5,6,7,8,9,10],
                         engine='python')
        first_col='startTime'
        if(data.iloc[0][first_col]==first_col):
            data= data.drop([0])
    except:
        try:
            data=pd.read_csv(file_path,
                 sep=',',
                 header='infer',
                 dtype = {'total distance':np.float64,
                          'energy consumed':np.float64},
                 parse_dates=['startTime','endTime'],
                 infer_datetime_format=True,
                 na_values=['total distance'],
                 error_bad_lines=False,
                 index_col=False,
                 quotechar='|',
                 usecols=[0,1,2,3,4,5,6,7,8,9,10],
                 engine='python')
            first_col='startTime'
            if(data.iloc[0][first_col]==first_col):
                data= data.drop([0])
        except:
            print("There was a problem loading:"+str(file_path))
            return None,None
    return cur_blob,data


def open_healthkit_sleep(file_path): 
    try:
        cur_blob=file_path.split('/')[-2]
    except: 
        return None,None
    try:
        data=pd.read_csv(file_path,
                         sep=',',
                         header='infer',
                         dtype = {'value': np.float64 },
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
                             dtype = {'value': np.float64 },
                             parse_dates=['startTime'],
                             infer_datetime_format=True,
                             quotechar='"',
                             na_values=['value'],
                             error_bad_lines=False,
                             index_col=False,
                             engine='python')
        except:
            print("There was a problem loading:"+str(file_path))
            return None,None    
    return cur_blob,data 

def open_motion_activity_synapse(file_path): 
    try:
        cur_blob=file_path.split('/')[-2]
    except: 
        return None,None,None
    try:
        pandas_columns=['startTime','activityType','confidence']
        data=pd.read_csv(file_path,
                         sep=',',
                         header='infer',
                         dtype={'value':np.float64},
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
                return None,None,None
    return cur_blob,data,parse_as


