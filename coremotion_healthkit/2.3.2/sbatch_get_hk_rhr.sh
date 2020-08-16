for i in `seq 0 152`
do
    #sherlock
    sbatch -J hk.rhr.$i -e logs_hk_rhr/$i.e -o logs_hk_rhr/$i.o -p akundaje,euan,owners,normal -t180 get_healthkit.DataCollector.RHR.sh $i
done


