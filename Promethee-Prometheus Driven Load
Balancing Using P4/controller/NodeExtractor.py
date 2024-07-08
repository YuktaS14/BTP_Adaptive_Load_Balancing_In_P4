import requests

# LoadMetrics = {}

def fetch_data(prometheus_url):
    try:
        response = requests.get(prometheus_url)
        response.raise_for_status()  # Raise HTTPError for bad status codes
        return response.text.split('\n')
    except requests.RequestException as e:
        print("Request Exception:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

def extract_metric_value(data, metric_name):
    metric_value = 0
    for line in data:
        if line.startswith(metric_name):
            metric_value += float(line.split()[1])
    return metric_value

def extract_metrics(prometheus_url, metric_name):
    data = fetch_data(prometheus_url)
    if data:
        return extract_metric_value(data, metric_name)
    else:
        return None

def bytes_to_mb(bytes_value):
    return bytes_value / (1024 * 1024)

def LoadMetrics(prometheus_url = 'http://127.0.1.1:9100/metrics'):
    # Prometheus URL

    # Metric names
    metrics = {
        'network_usage': 'node_network_transmit_bytes_total',  # Network usage
        'cpu_load': 'node_load1',   # CPU load
        'ram_usage': 'node_memory_Active_bytes' # RAM usage
        #'disk_io_usage': 'node_disk_io_time_seconds_total',  # Disk I/O usage
        #'disk_space_usage': 'node_filesystem_size_bytes',  # Disk space usage
        # 'process_count': 'node_processes_running',  # Number of processes running
        # 'uptime_seconds': 'node_time_seconds',  # System uptime
    }

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
    # print("Load balancing metrics:")
    # for metric_name, metric_value in load_metrics.items():
    #     print(f"{metric_name}: {metric_value}")

    return load_metrics


# LoadMetrics = main()
