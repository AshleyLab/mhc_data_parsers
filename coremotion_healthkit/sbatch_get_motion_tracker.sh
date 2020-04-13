for i in `seq 0 184`
do
    sbatch -J motion.tracker.$i -e logs_motion_tracker/$i.e -o logs_motion_tracker/$i.o -p euan,akundaje,owners,normal -t60 get_motion_tracker.sh $i
done
