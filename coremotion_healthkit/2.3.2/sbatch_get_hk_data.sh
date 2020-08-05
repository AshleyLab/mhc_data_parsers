#for i in `seq 0 139`
#for i in 105 112 118 122 124 127 128 129 12 130 131 132 133 134 135 136 138 139 17 19 21 37 53 59 6 84 86 95 
#for i in 127 128 129 130 131 132 133 134 135 136 138 139 37 53 59 84
for i in 122 12 17 19 21 86
do
    #sherlock
    sbatch -J hk.data.$i -e logs_hk_data/$i.e -o logs_hk_data/$i.o -p akundaje,euan,owners,normal -t180 get_healthkit.DataCollector.sh $i
    #scg
    #sbatch -J hk.data.$i -e logs_hk_data/$i.e -o logs_hk_data/$i.o --account akundaje -t180 get_healthkit.DataCollector.sh $i
done


