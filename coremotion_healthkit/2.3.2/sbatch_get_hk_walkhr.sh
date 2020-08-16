for i in `seq 0 152`
do
    #sherlock
    sbatch -J hk.walkhr.$i -e logs_hk_walkinghr/$i.e -o logs_hk_walkinghr/$i.o -p akundaje,euan,owners,normal -t100 get_healthkit.DataCollector.WalkingHR.sh $i
done


