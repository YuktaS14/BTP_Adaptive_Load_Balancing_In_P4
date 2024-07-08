#!/bin/bash

# Define the Python file to run
python_file="client.py"

# Define the number of times to run the Python file
num_runs=100

# Loop to run the Python file 50 times
for ((i=1; i<=$num_runs; i++)); do
    echo "Running $python_file for the $i time"
    python3 $python_file &
    # iperf -c 10.0.0.
    sleep 1
done

echo "All $num_runs runs completed"