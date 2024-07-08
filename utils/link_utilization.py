import time
import psutil

def calculate_network_bandwidth_utilization(in_bytes_prev, out_bytes_prev, time_prev):
  """
  Calculates network bandwidth utilization for incoming and outgoing traffic since the previous measurement.

  Args:
      in_bytes_prev: Number of bytes received during the previous measurement interval.
      out_bytes_prev: Number of bytes transmitted during the previous measurement interval.
      time_prev: Start time of the previous measurement interval (seconds).

  Returns:
      A tuple containing the incoming and outgoing bandwidth utilization percentages.
  """

  # Get current network statistics
  net = psutil.net_io_counters()
  in_bytes = net.bytes_recv
  out_bytes = net.bytes_sent

  # Calculate time difference since previous measurement
  current_time = time.time()
  time_diff = current_time - time_prev

  # Check if enough time has passed for a new measurement
  if time_diff < 5:
    return None  # Not enough time passed, return None

  # Calculate utilization percentages for the interval
  in_utilization = ((in_bytes - in_bytes_prev) * 8) / (time_diff * line_speed) * 100
  out_utilization = ((out_bytes - out_bytes_prev) * 8) / (time_diff * line_speed) * 100

  return in_utilization, out_utilization

# Initialize variables for the first run
in_bytes_prev = 0
out_bytes_prev = 0
time_prev = time.time()
line_speed = 10000000  # 10 Mbps

while True:
  # Get bandwidth utilization
  utilization = calculate_network_bandwidth_utilization(in_bytes_prev, out_bytes_prev, time_prev)

  if utilization is not None:
    in_utilization, out_utilization = utilization
    print(f"Incoming bandwidth utilization: {in_utilization:.2f}%")
    print(f"Outgoing bandwidth utilization: {out_utilization:.2f}%")

  # Update variables for next measurement
  in_bytes_prev = psutil.net_io_counters().bytes_recv
  out_bytes_prev = psutil.net_io_counters().bytes_sent
  time_prev = time.time()

  # Sleep for 5 seconds before next measurement
  time.sleep(5)
