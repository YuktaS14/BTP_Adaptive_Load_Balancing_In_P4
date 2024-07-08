from prometheus_api_client import PrometheusConnect
import json

prometheus_url = "http://127.0.1.1:9090"

p_connect = PrometheusConnect(url=prometheus_url)

query = 'avg_over_time(100 - (avg by(instance)(irate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)[1m:])'

resp = p_connect.custom_query(query)

print(resp)

# try:
#     resp = p_connect.custom_query(query)
#     for i in resp:
#         print(i['metric'])
#         print(i['value'])
# except json.JSONDecodeError as e:
#         print("Error: Failed to decode JSON response:", e)
# # print(resp)
