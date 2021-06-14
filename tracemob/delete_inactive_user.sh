# !/bin/sh
# . /root/anaconda3/etc/profile.d/conda.sh
. /vat/opt/miniconda3/etc/profile.d/conda.sh
conda activate emission
cd '/var/emission/e-mission-server/'

OUTPUT='/var/tmp/delete_inactive_user_out.txt'
start=`date +%s`
case $@ in
    *"-console"*)
        ./e-mission-py.bash tracemob/delete_inactive_user.py
        ;;
    *)
        ./e-mission-py.bash tracemob/delete_inactive_user.py &> $OUTPUT &
        PID=$!
        echo 'PID:' $PID
        ps -ef | grep -w $PID | grep -v grep
        ;;
esac
end=`date +%s`
echo "delete_inactive_user $((end-start))sec" >> '/var/log/emission/elapsedtime.log'
