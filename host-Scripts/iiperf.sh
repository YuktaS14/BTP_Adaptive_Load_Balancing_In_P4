#!/bin/bash

for i in {1..100}; 
do
    echo $i
    iperf -c 10.0.0.52 -t 50 &  # Run iperf in the background
    sleep 1  # Wait for 1 second
done