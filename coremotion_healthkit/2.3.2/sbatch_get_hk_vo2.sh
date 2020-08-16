for i in `seq 0 152`
do
    #sherlock
    sbatch -J hk.vo2.$i -e logs_hk_vo2/$i.e -o logs_hk_vo2/$i.o -p akundaje,euan,owners,normal -t100 get_healthkit.VO2.sh $i
done


