for i in `seq 0 152`
do
    #sherlock
    sbatch -J hk.bp.$i -e logs_hk_bp/$i.e -o logs_hk_bp/$i.o -p akundaje,euan,owners,normal -t180 get_healthkit.bp.sh $i
done


