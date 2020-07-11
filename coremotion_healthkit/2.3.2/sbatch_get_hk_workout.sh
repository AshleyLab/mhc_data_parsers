for i in `seq 0 59`
do
    #sherlock
    sbatch -J hk.workout.$i -e logs_hk_workout/$i.e -o logs_hk_workout/$i.o -p euan,akundaje,owners,normal -t60 get_healthkit.Workout.sh $i
    #scg
    #sbatch -J hk.workout.$i -e logs_hk_workout/$i.e -o logs_hk_workout/$i.o --account akundaje -t60 get_healthkit.Workout.sh $i
done
