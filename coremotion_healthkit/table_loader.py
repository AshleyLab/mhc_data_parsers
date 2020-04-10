#Author: annashch@stanford.edu
import numpy as np
import pandas as pd 
from datetime import datetime
from dateutil.parser import parse 

def convert_datetime(x):
    if x=="NA":
        return np.nan
    else:
        return parse(x)
    
def convert_int(x):
    if x=="NA":
        return np.nan
    else:
        return int(float(x)) 

def convert_float(x):
    if x=="NA":
        return np.nan
    else:
        return float(x)     
    

def load_table(table_path):
    data= pd.read_csv(table_path,
                      sep='\t',
                      header=0,
                      quotechar='"',
                      index_col=0,
                      dtype={'data.csv':str,
                             'rawData':str,
                             4:str,
                             12:str},
                      parse_dates=['uploadDate','createdOn'],
                      infer_datetime_format=True,
                      error_bad_lines=False,
                      engine='c')
    return data 
if __name__=="__main__":
    #TESTS for sherlock
    import pdb
    base_dir="/oak/stanford/groups/euan/projects/mhc/data/tables/"
    motionactivity_data=load_table(base_dir+"cardiovascular-motionActivityCollector-v1.tsv")
    healthkit_data=load_table(base_dir+"cardiovascular-HealthKitDataCollector-v1.tsv")
    pdb.set_trace()
    
