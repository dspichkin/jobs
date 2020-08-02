#!/usr/bin/env bash

# run py.test ($@ to derive parameters from commandline)
python get_data.py $@ &
pid="$!"

# trap process id to stop script using Control+C
trap "echo '=== Stopping PID $pid ==='; kill -SIGTERM $pid" SIGINT SIGTERM
echo $pid
wait $pid