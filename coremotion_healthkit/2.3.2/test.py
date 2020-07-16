import pandas as pd 
import numpy as np 
import pdb 
file_path="/oak/stanford/groups/euan/projects/mhc/data/synapseCache/206/54023206/UA85W-3sTuKDYu7Nf5RcE2_U-data.csv"
data=pd.read_csv(file_path,
                 sep=',',
                 names=['startTime','type','category','value','unit','source','sourceIdentifier','appVersion'],
                 header=None,
                 dtype = {'value': np.float16 },
                 parse_dates=['startTime'],
                 infer_datetime_format=True,
                 quotechar='"',
                 na_values=['value'],
                 error_bad_lines=False,
                 index_col=False,
                 engine='python')
pdb.set_trace() 
