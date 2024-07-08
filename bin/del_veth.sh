#!/bin/bash

for idx in 0 1 2 3 4; do
    intf0="veth$(($idx*2))"
    intf1="veth$(($idx*2+1))"
    
    # Check if the interface exists before trying to delete
    if ip link show $intf0 &> /dev/null; then
        ip link delete $intf0
    fi
    if ip link show $intf1 &> /dev/null; then
        ip link delete $intf1
    fi
done