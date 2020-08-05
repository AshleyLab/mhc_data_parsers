for i in `seq 0 139`
do
    #sherlock
    sbatch -J hk.rhr.$i -e logs_hk_rhr/$i.e -o logs_hk_rhr/$i.o -p akundaje,euan,owners,normal -t180 get_healthkit.HR.sh $i
    #scg
    #sbatch -J hk.data.$i -e logs_hk_data/$i.e -o logs_hk_data/$i.o --account akundaje -t180 get_healthkit.DataCollector.sh $i
done


