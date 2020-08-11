#for i in `seq 0 152`
for i in 130 
do
    #sherlock
    sbatch -J hk.data.$i -e logs_hk_data/$i.e -o logs_hk_data/$i.o -p akundaje,euan,normal -t300 get_healthkit.DataCollector.sh $i
    #scg
    #sbatch -J hk.data.$i -e logs_hk_data/$i.e -o logs_hk_data/$i.o --account akundaje -t180 get_healthkit.DataCollector.sh $i
done


