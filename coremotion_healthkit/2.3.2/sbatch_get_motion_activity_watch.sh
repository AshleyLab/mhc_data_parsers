for i in `seq 0 20`
do
    #sherlock
    sbatch -J motion.activity.$i -e logs_motion_activity_watch/$i.e -o logs_motion_activity_watch/$i.o -p euan,akundaje,owners,normal -t60 get_motion_activity_watch.sh $i
    #scg
    #sbatch -J motion.activity.$i -e logs_motion_activity_watch/$i.e -o logs_motion_activity_watch/$i.o --account akundaje -t60 get_motion_activity_watch.sh $i
done
