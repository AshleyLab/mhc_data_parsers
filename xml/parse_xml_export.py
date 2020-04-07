import argparse 
import xmltodict 
import pandas as pd 
ignore={} 
ignore['MetadataEntry']=True
ignore['#text']=True
ignore['HeartRateVariabilityMetadataList']=True


def parse_args(): 
    parser=argparse.ArgumentParser(description="parse healthkit xml export file")
    parser.add_argument('--xmlfile')
    parser.add_argument('--out_prefix') 
    return parser.parse_args() 


def parse_me(me,out_prefix): 
    df=pd.DataFrame.from_dict(me,orient='index') 
    df.to_csv(out_prefix+'.personal.txt',sep='\t',header=False,index=False)
    
def parse_records(records,out_prefix): 
    #combine records into dataframe so all columns are matching order 
    df=pd.DataFrame(records) 
    for col in ignore: 
        if col in df.columns: 
            print("dropping:"+str(col))
            df=df.drop([col],axis=1)
    #get the unique set of record types 
    record_types=list(set(df['@type'].tolist()))
    #create an output file for each record type 
    for record_type in record_types: 
        print(record_type) 
        sub_df=df[df['@type']==record_type]
        sub_df.to_csv(out_prefix+".records."+record_type+".txt",sep='\t',header=True,index=False)
    

def parse_workouts(workouts,out_prefix): 
    #combine records into dataframe so all columns are matching order 
    df=pd.DataFrame(workouts) 
    for col in ignore: 
        if col in df.columns:
            print("dropping:"+str(col))
            df=df.drop([col],axis=1)
    #get the unique set of record types 
    workout_types=list(set(df['@workoutActivityType'].tolist()))
    #create an output file for each record type 
    for workout_type in workout_types: 
        print(workout_type) 
        sub_df=df[df['@workoutActivityType']==workout_type]
        sub_df.to_csv(out_prefix+".workouts."+workout_type+".txt",sep='\t',header=True,index=False)

def main(): 
    args=parse_args()
    print("loading xml file to python dict:")
    with open(args.xmlfile) as fd: 
        doc=xmltodict.parse(fd.read())['HealthData'] 
    print("xmldict loaded") 
    print("parsing personal data:")
    me=doc['Me'] 
    print("personal data parsed")
    parse_me(me,args.out_prefix) 
    print("parsing records") 
    records=doc['Record'] 
    parse_records(records,args.out_prefix) 
    print("records parsed") 
    print("parsing workouts:")
    workouts=doc['Workout'] 
    parse_workouts(workouts,args.out_prefix) 
    print("workouts parsed")
    print("done!") 
    
if __name__=="__main__": 
    main() 
