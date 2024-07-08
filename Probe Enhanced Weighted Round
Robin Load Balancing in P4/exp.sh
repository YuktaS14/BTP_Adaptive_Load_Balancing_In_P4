#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 exp_t_sec probe_time_period"
    exit 1
fi

# Assign arguments to variables
t_sec=$1
probe_time_period=$2

# Check if t_sec is less than or equal to probe_time_period
if [ "$t_sec" -le "$probe_time_period" ]; then
    echo "Error: exp_t_sec should be greater than probe_time_period."
    exit 1
fi

# Start the server
echo "Starting server..."
sudo python server.py $t_sec $probe_time_period&

# Capture the PID of the server
server_pid=$!

# Start the probe
echo "Starting probes..."
sudo python probe.py $t_sec $probe_time_period &

# Capture the PID of the probe
probe_pid=$!

# Wait for some time
sleep ($t_sec + 10)

# Kill the server and probe
echo "Closing server and probe..."
kill $server_pid $probe_pid

echo "Server and probe closed."
