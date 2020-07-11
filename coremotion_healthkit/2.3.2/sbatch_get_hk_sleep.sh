for i in `seq 0 62`
do
    #sherlock
    sbatch -J hk.sleep.$i -e logs_hk_sleep/$i.e -o logs_hk_sleep/$i.o -p euan,akundaje,owners,normal -t60 get_healthkit.Sleep.sh $i
    #scg
    #sbatch -J hk.sleep.$i -e logs_hk_sleep/$i.e -o logs_hk_sleep/$i.o --account akundaje -t60 get_healthkit.Sleep.sh $i
done
