from datetime import datetime,timedelta,date
from dateutil.parser import parse

def qc_hk(datatype,value,startTime,endTime):
    #datatype=datatype.decode('utf-8') 
    if datatype not in ["HKQuantityTypeIdentifierDistanceWalk","HKQuantityTypeIdentifierStepCount"]:
        return True 
    try:
        if type(startTime)==str: 
            startTime=parse(startTime)
        if type(endTime)==str: 
            endTime=parse(endTime) 
    except: 
        return False 
    if datatype=="HKQuantityTypeIdentifierDistanceWalk": 
        try:
            time_diff=(endTime-startTime).total_seconds()/60.0
        except: 
            return False 
        speed=value/time_diff
        if speed > 750: 
            print('BAD SPEED') 
            return False 
        else: 
            return True 
    if datatype=="HKQuantityTypeIdentifierStepCount": 
        try:
            time_diff=(endTime-startTime).total_seconds()/60.0
        except: 
            return False 
        if time_diff==0: 
            return True
        rate=value/time_diff 
        if rate >1000: 
            print("BAD RATE") 
            return False 
        else: 
            return True 
