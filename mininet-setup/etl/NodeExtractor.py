import requests

def extract_metrics(prometheus_url, metric_name):
    try:
        response = requests.get(prometheus_url)
        if response.status_code == 200:
            data = response.text.split('\n')
            metric_value = 0
            for line in data:
                if line.startswith(metric_name):
                    metric_value += float(line.split()[1])
            return metric_value
        else:
            print("Failed to fetch data from Prometheus. Status code:", response.status_code)
            return None
    except requests.RequestException as e:
        print("Request Exception:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

# Prometheus URL
prometheus_url = 'http://127.0.1.1:9100/metrics'

# Metric names
metrics = {
    'cpu_load': 'node_load1',   # CPU load
    'ram_usage': 'node_memory_Active_bytes',  # RAM usage
    'network_usage': 'node_network_receive_bytes_total',  # Network usage
    'disk_io_usage': 'node_disk_io_time_seconds_total',  # Disk I/O usage
    'disk_space_usage': 'node_filesystem_size_bytes',  # Disk space usage
    # 'process_count': 'node_processes_running',  # Number of processes running
    'uptime_seconds': 'node_time_seconds',  # System uptime
}

# Convert bytes to megabytes
def bytes_to_mb(bytes_value):
    return bytes_value / (1024 * 1024)

# Extract metrics
load_metrics = {}
for metric_name, prometheus_metric_name in metrics.items():
    metric_value = extract_metrics(prometheus_url, prometheus_metric_name)
    if metric_value is not None:
        # Convert network usage to megabytes
        if metric_name == 'network_usage':
            metric_value = bytes_to_mb(metric_value)
        load_metrics[metric_name] = metric_value
    else:
        print(f"Failed to extract {metric_name} data from Prometheus.")

# Display metrics
print("Load balancing metrics:")
for metric_name, metric_value in load_metrics.items():
    print(f"{metric_name}: {metric_value}")
