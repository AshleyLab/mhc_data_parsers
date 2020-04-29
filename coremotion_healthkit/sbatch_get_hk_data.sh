for i in `seq 0 178`
do
    sbatch -J hk.data.$i -e logs_hk_data/$i.e -o logs_hk_data/$i.o -p akundaje,owners,normal -t60 get_healthkit.DataCollector.sh $i
done
