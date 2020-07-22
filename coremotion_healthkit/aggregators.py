from datetime import datetime,timedelta
from dateutil.parser import parse
import pdb 

def aggregate_motion_tracker(subject_blob_vals,outf_prefix):     
    outf=open(outf_prefix,'w')
    outf.write('Subject\tDate\tWeekday\tActivity\tDuration_in_Minutes\tFraction\tNumentries\tSourceBlobs\n')
    for cur_subject in subject_blob_vals: 
        for cur_aggregation_interval in subject_blob_vals[cur_subject]: 
            cur_weekday=cur_aggregation_interval.weekday() 
            total_minutes=subject_blob_values[cur_subject][cur_aggregation_interval]['TotalMinutes']
            for cur_activity in subject_blob_vals[cur_subject][cur_aggregation_interval]: 
                if cur_activity=="TotalMinutes":
                    continue
                cur_activity_minutes=subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['Minutes']
                cur_activity_fraction=cur_activity_minutes/(total_minutes+.001) #add pseudocount to avoid division by 0 
                cur_activity_entries=subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['N']
                cur_activity_blobs=','.join([str(i) for i in subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['Blobs']])

                outf.write(cur_subject+'\t'+
                           str(cur_aggreagtion_interval)+'\t'+
                           str(cur_weekday)+'\t'+
                           cur_activity+'\t'+
                           str(cur_activity_minutes)+'\t'+
                           str(cur_activity_fraction)+'\t'+
                           str(cur_activity_entries)+'\t'+
                           str(cur_activity_blobs)+'\n')
    outf.close()            
                    
def aggregate_healthkit_data_collector(subject_blob_vals,outf_prefix):
    outf=open(outf_prefix,'w')
    outf.write("Subject\tDate\tWeekDay\tMetric\tN\tSum\tMin\tMax\tMean\tSource\tSourceBlobs\n")
    for cur_subject in subject_blob_vals: 
        for cur_aggregation_interval in subject_blob_vals[cur_subject]: 
            cur_weekday=cur_aggregation_interval.weekday()
            for datatype in subject_blob_vals[cur_subject][cur_aggregation_interval]: 
                for source_tuple in subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]: 
                    minval=subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Min']
                    maxval=subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Max']
                    sumvals=subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Sum']
                    nvals=subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['N']
                    if nvals==0: 
                        nvals+=0.001  #add pseudocount to avoid division by 0 
                    meanvals=round(sumvals/nvals,2)
                    blobs=','.join([str(i) for i in subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Blobs']])
                    outf.write(cur_subject+'\t'+
                               str(cur_aggregation_interval)+'\t'+
                               str(cur_weekday)+'\t'+
                               str(datatype)+'\t'+
                               str(nvals)+'\t'+
                               str(sumvals)+'\t'+
                               str(minval)+'\t'+
                               str(maxval)+'\t'+
                               str(meanvals)+'\t'+
                               str(','.join(source_tuple))+'\t'+
                               str(blobs)+'\n')
    outf.close()

def aggregate_duplicate_timestamp_blobs(subject_timestamp_blobs,outf_prefix):
    outf=open(outf_prefix+".duplicate.timestamps",'w')
    outf.write('Subject\tRow\tBlobs\n')
    for subject in subject_timestamp_blobs: 
        for row_hash in subject_timestamp_blobs[subject]:
            if len(subject_timestamp_blobs[subject][row_hash])>1:
                #there are duplicates for this row 
                cur_row=subject_timestamp_blobs[subject][row_hash][0]
                blobs=subject_timestamp_blobs[subject][row_hash][1::]
                while cur_row in blobs: 
                    blobs.remove(cur_row) 
                outf.write(subject+'\t'+cur_row+'\t'+','.join(blobs)+'\n')
    outf.close()
