import psutil
import time
from scapy.all import *
import sys
import os
from datetime import datetime

class CustomHeader(Packet):
    fields_desc = [
        BitField("id", 0, 4),
        BitField("cpu_percent", 0, 4),
        BitField("memory_percent", 0, 4),
        BitField("link_util", 0, 4),
    ]

bind_layers(IP, CustomHeader, proto=0x42)

LINESPEED = 10000000  # Assuming bw 10 Mbps

def get_system_metrics(in_bytes_prev, out_bytes_prev, time_prev):
    cpu_percent = int((100 - int(psutil.cpu_percent())) / 10)
    memory_percent = int((100 - int(psutil.virtual_memory().percent)) / 10)

    cur_time = time.time()
    time_diff = cur_time - time_prev

    if time_diff < TIMEPERIOD:
        print(cpu_percent, memory_percent, 0)
        return cpu_percent, memory_percent, 0 

    in_bytes_recv = psutil.net_io_counters().bytes_recv
    out_bytes_sent = psutil.net_io_counters().bytes_sent

    in_util = ((in_bytes_recv - in_bytes_prev) * 8) / (time_diff * LINESPEED) * 100
    out_util = ((out_bytes_sent - out_bytes_prev) * 8) / (time_diff * LINESPEED) * 100

    in_util_left = int((100 - in_util) / 10)
    out_util_left = int((100 - out_util) / 10)

    link_util = in_util_left

    throughput = (in_bytes_recv - in_bytes_prev + out_bytes_sent - out_bytes_prev)

    print(cpu_percent, memory_percent, link_util, throughput)
    return cpu_percent, memory_percent, link_util, throughput, cur_time, in_bytes_recv, out_bytes_sent, time_diff

def get_if():
    ifs = get_if_list()
    iface = None
    for i in ifs:
        if "eth0" in i:
            iface = i
            break
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

def send_metrics_to_host(cpu_percent, memory_percent, link_util, dstEth, iface, id, probe_count):
    print("sending .........")
    hw_if = get_if_hwaddr(iface)
    pkt = Ether(src=hw_if, dst=dstEth) / IP() / CustomHeader(id=1, cpu_percent=cpu_percent,
                                                             memory_percent=memory_percent, link_util=link_util)
    pkt = pkt / Raw("probe packet")
    pkt[IP].proto = 42
    sendp(pkt, iface=iface, verbose=False)
    print("Probe Count:", probe_count)

def write_throughput_to_file(start_time, end_time, throughput_value, probe_count):
    start_time_str = datetime.fromtimestamp(start_time).strftime('%d/%m/%Y %H:%M:%S')
    end_time_str = datetime.fromtimestamp(end_time).strftime('%d/%m/%Y %H:%M:%S')
    with open("throughput.txt", "a") as file:
        file.write("Start Time: %s, End Time: %s, Throughput: %.2f KB/sec, Probe Count: %d, Probe_freq: %s, run_time: %s\n" % (
            start_time_str,
            end_time_str,
            throughput_value / 1024.0,  # Dividing by 1024 to convert bytes to KB
            probe_count,
            sys.argv[2],
            sys.argv[1]
        ))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <time_in_seconds> <probe timeperiod>")
        sys.exit(1)

    TIMEPERIOD = float(sys.argv[2])
    total_time_to_run = float(sys.argv[1])
    timeout = float(sys.argv[3])
    start_time = time.time()
    end_time = start_time + total_time_to_run

    print("Metrics")
    dst_mac = "12:30:2e:17:03:d9"
    id_val = 1
    iface = "enp0s3"
    in_bytes_prev = psutil.net_io_counters().bytes_recv
    out_bytes_prev = psutil.net_io_counters().bytes_sent

    time_prev = time.time()
    start_time = time.time()
    probe_count = 0
    throughput = 0
    #iteration = 1
    total_iterations = int(timeout/TIMEPERIOD)
    total_throughput = []
    total_cpu = []
    total_mem = []
    total_link = []
    time.sleep(TIMEPERIOD)

    try:
        while time.time() < end_time:
            cpu_percent, memory_percent, link_util, throughput, time_prev, in_bytes_prev, out_bytes_prev, time_diff = get_system_metrics(in_bytes_prev, out_bytes_prev,
                                                                                    time_prev)

            val = throughput / time_diff
            print("Throughput at time :", time_prev, " = ", val , "bytes/s")
            total_throughput.append(val)
            total_cpu.append(cpu_percent)
            total_mem.append(memory_percent)
            total_link.append(link_util)
            probe_count += 1
            s = time.time()
            send_metrics_to_host(cpu_percent, memory_percent, link_util, dst_mac, iface, id_val,
                                 probe_count)
            
            #if(iteration == total_iterations):
                #average_throughput = sum(total_throughput)/len(total_throughput)
                #write_throughput_to_file(start_time, time.time(), average_throughput, probe_count)
                #iteration = 0     
            #iteration += 1
            time.sleep(TIMEPERIOD)

        #average_throughput = sum(total_throughput)/len(total_throughput)
        #print("Total Throughput:", average_throughput, "bytes/s")
    except KeyboardInterrupt:
        average_throughput = sum(total_throughput)/len(total_throughput)
        average_cpu = sum(total_cpu)/len(total_cpu)
        average_mem = sum(total_mem)/len(total_mem)
        average_link = sum(total_link)/len(total_link)
        print("\nProgram interrupted by user.")
        print("Average Throughput:", average_throughput, "bytes/s")
        print("Average CPU left:", average_cpu*10, "%")
        print("Average Memory left:", average_mem*10, "%")
        print("Average LinkUtilization left:", average_link*10, "%")

