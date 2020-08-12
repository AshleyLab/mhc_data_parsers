for i in 86
do
    sbatch -J hk.data.$i -e logs_hk_data/$i.e -o logs_hk_data/$i.o -p akundaje,euan,normal,owners -t180 get_healthkit.DataCollector.hr1440.sh $i
done



