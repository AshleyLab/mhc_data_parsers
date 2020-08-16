for i in `seq 0 152`
do
    #sherlock
    sbatch -J hk.data.$i -e logs_hk_var/$i.e -o logs_hk_var/$i.o -p akundaje,euan,normal -t100 get_healthkit.DataCollector.HRVariability.sh $i
done


