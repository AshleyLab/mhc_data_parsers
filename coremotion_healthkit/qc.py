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
