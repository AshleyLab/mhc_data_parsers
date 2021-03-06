from datetime import datetime,timedelta
from dateutil.parser import parse
import statistics
import pdb 

def aggregate_motion_tracker(subject_blob_vals,outf_prefix,get_median=False):     
    outf=open(outf_prefix,'w')
    outf.write('Subject\tDate\tWeekday\tActivity\tDuration_in_Minutes\tFraction\tNumentries\tSourceBlobs\n')
    for cur_subject in subject_blob_vals: 
        for cur_aggregation_interval in subject_blob_vals[cur_subject]: 
            cur_weekday=cur_aggregation_interval.weekday() 
            total_minutes=subject_blob_vals[cur_subject][cur_aggregation_interval]['TotalMinutes'].seconds/60
            for cur_activity in subject_blob_vals[cur_subject][cur_aggregation_interval]: 
                if cur_activity=="TotalMinutes":
                    continue
                cur_activity_minutes=subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['Minutes'].seconds/60
                cur_activity_fraction=cur_activity_minutes/(total_minutes+.001) #add pseudocount to avoid division by 0 
                cur_activity_entries=subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['N']
                cur_activity_blobs=','.join([str(i) for i in subject_blob_vals[cur_subject][cur_aggregation_interval][cur_activity]['Blobs']])

                outf.write(cur_subject+'\t'+
                           str(cur_aggregation_interval)+'\t'+
                           str(cur_weekday)+'\t'+
                           cur_activity+'\t'+
                           str(cur_activity_minutes)+'\t'+
                           str(cur_activity_fraction)+'\t'+
                           str(cur_activity_entries)+'\t'+
                           str(cur_activity_blobs)+'\n')
    outf.close()            
                    
def aggregate_healthkit_data_collector(subject_blob_vals,outf_prefix,get_median=False):
    outf=open(outf_prefix,'w')
    outf.write("Subject\tDate\tWeekDay\tMetric\tN\tSum\tMin\tMax\tMean\tSource\tSourceBlobs")
    if get_median is True: 
        outf.write("\tMedian\n")
    else: 
        outf.write("\n") 
    for cur_subject in subject_blob_vals: 
        for cur_aggregation_interval in subject_blob_vals[cur_subject]: 
            cur_weekday=cur_aggregation_interval.weekday()
            for datatype in subject_blob_vals[cur_subject][cur_aggregation_interval]: 
                for source_tuple in subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]: 
                    minval=subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Min']
                    maxval=subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Max']
                    sumvals=subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Sum']
                    nvals=subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['N']
                    if get_median is True: 
                        median_val=statistics.median(subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Median'])
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
                               ','.join([str(i) for i in source_tuple])+'\t'+
                               str(blobs))
                    if get_median is True: 
                        outf.write('\t'+str(median_val))
                    outf.write('\n')
    outf.close()
def aggregate_healthkit_workout_collector(subject_blob_vals,outf_prefix,get_median=False):
    outf=open(outf_prefix,'w')
    outf.write("Subject\tDate\tWeekDay\tMetric\tN\tDistance\tEnergy\tSource\tSourceBlobs\n")
    for cur_subject in subject_blob_vals: 
        for cur_aggregation_interval in subject_blob_vals[cur_subject]: 
            cur_weekday=cur_aggregation_interval.weekday()
            for datatype in subject_blob_vals[cur_subject][cur_aggregation_interval]: 
                for source_tuple in subject_blob_vals[cur_subject][cur_aggregation_interval][datatype]: 
                    distance=subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Distance']
                    energy=subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Energy']
                    nvals=subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['N']
                    if nvals==0: 
                        nvals+=0.001  #add pseudocount to avoid division by 0 
                    blobs=','.join([str(i) for i in subject_blob_vals[cur_subject][cur_aggregation_interval][datatype][source_tuple]['Blobs']])
                    outf.write(cur_subject+'\t'+
                               str(cur_aggregation_interval)+'\t'+
                               str(cur_weekday)+'\t'+
                               str(datatype)+'\t'+
                               str(nvals)+'\t'+
                               str(distance)+'\t'+
                               str(energy)+'\t'+
                               str(','.join([str(i) for i in source_tuple]))+'\t'+
                               str(blobs)+'\n')
    outf.close()

def aggregate_duplicate_timestamp_blobs(subject_timestamp_blobs,outf_prefix):
    outf=open(outf_prefix+".duplicate.timestamps",'w')
    outf.write('Subject\tRow\tBlobs\n')
    for subject in subject_timestamp_blobs: 
        for row in subject_timestamp_blobs[subject]:
            if len(subject_timestamp_blobs[subject][row])>1:
                blobs=subject_timestamp_blobs[subject][row] 
                outf.write(str(subject)+'\t'+str(row)+'\t'+','.join([str(i) for i in blobs])+'\n')
    outf.close()
