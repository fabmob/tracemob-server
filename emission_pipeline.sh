# !/bin/sh
# . /root/anaconda3/etc/profile.d/conda.sh
. /vat/opt/miniconda3/etc/profile.d/conda.sh
conda activate emission
cd '/var/emission/e-mission-server/'

OUTPUT='/var/tmp/intake_out.txt'
start=`date +%s`
case $@ in
    *"-console"*)
        ./e-mission-py.bash bin/intake_multiprocess.py 3
        ;;
    *)
        ./e-mission-py.bash bin/intake_multiprocess.py 3 &> $OUTPUT &
        PID=$!
        echo 'PID:' $PID
        ps -ef | grep -w $PID | grep -v grep
        ;;
esac
end=`date +%s`
echo "emission_pipeline $((end-start))sec" >> '/var/log/emission/elapsedtime.log'
