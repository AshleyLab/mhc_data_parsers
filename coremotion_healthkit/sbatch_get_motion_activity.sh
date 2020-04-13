for i in `seq 0 140`
do
    sbatch -J motion.activity.$i -e logs_motion_activity/$i.e -o logs_motion_activity/$i.o -p euan,akundaje,owners,normal -t60 get_motion_activity.sh $i
done
