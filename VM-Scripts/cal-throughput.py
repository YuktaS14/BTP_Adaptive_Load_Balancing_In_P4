import psutil
import time

INTERFACE_NAME = "enp0s3"  # Replace with your actual interface name
MEASUREMENT_INTERVAL = 20  # Seconds

def get_interface_throughput(interface_name):
    """Gets the bytes sent and received for a specific network interface."""
    net_io = psutil.net_io_counters(pernic=True)
    if interface_name in net_io:
        return net_io[interface_name].bytes_sent, net_io[interface_name].bytes_recv
    else:
        raise ValueError("Interface '%s' not found." % interface_name)  # String formatting for Python 2.7

max_sent = 0
max_recv = 0

while True:
    try:
        start_sent, start_recv = get_interface_throughput(INTERFACE_NAME)
        time.sleep(MEASUREMENT_INTERVAL)
        end_sent, end_recv = get_interface_throughput(INTERFACE_NAME)

        # Calculate throughput in kilobits per second (Kb/s)
        throughput_sent = (end_sent - start_sent) * 8.0 / (MEASUREMENT_INTERVAL * 1024) # 8.0 to get float
        throughput_recv = (end_recv - start_recv) * 8.0 / (MEASUREMENT_INTERVAL * 1024)

        # Update maximum throughput values
        max_sent = max(throughput_sent, max_sent)
        max_recv = max(throughput_recv, max_recv)

        # Print throughput, using string formatting for better clarity
        print "Throughput Sent: %.2f Kb/s (Max: %.2f Kb/s)" % (throughput_sent, max_sent)
        print "Throughput Received: %.2f Kb/s (Max: %.2f Kb/s)" % (throughput_recv, max_recv)
        print "-" * 40 

    except ValueError as e:
        print e
        break  # Exit loop if the interface disappears
