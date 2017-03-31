#/bin/bash
TOTAL_PROCESS=4
for (( i = 0; i < $TOTAL_PROCESS; i++));
do
    nohup python thread-tb.py $i $TOTAL_PROCESS &
done

