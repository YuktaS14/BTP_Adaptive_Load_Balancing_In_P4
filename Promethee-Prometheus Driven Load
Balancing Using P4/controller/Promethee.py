from Ahp import weights
import numpy as np
from pymcdm.methods import PROMETHEE_II
from pymcdm.helpers import rrankdata
import time
from prometheus_api_client import PrometheusConnect

weight = weights

def GetRank():

    print('IN PROMETHEE')

    # print('AHP Weights -->' , weight.target_weights)

    wts = list(weight.target_weights.values())

    # vm1_values = list(LoadMetrics(prometheus_url = 'http://127.0.1.1:9501/metrics').values())

    # vm2_values = list(LoadMetrics(prometheus_url = 'http://127.0.1.1:9502/metrics').values())

    # vm3_values = list(LoadMetrics(prometheus_url = 'http://127.0.1.1:9503/metrics').values())

    # vm4_values = list(LoadMetrics(prometheus_url = 'http://127.0.1.1:9504/metrics').values())

    prometheus_url = "http://127.0.1.1:9090"

    p_connect = PrometheusConnect(url=prometheus_url)

    query = 'avg_over_time(100 - (avg by(instance)(irate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)[1m:])'

    resp = p_connect.custom_query(query)

    result = {}

    for entry in resp:

        instance = entry['metric']['instance']
        if 'localhost' not in instance:
            value = entry['value'][1]
            result[instance] = []
            result[instance].append(value)

    # print(result)

    query = '((node_memory_MemFree_bytes + node_memory_Cached_bytes + node_memory_Buffers_bytes) / node_memory_MemTotal_bytes) * 100'

    resp = p_connect.custom_query(query)

    for entry in resp:
        instance = entry['metric']['instance']
        if 'localhost' not in instance:
            value = entry['value'][1]
            result[instance].append(value)

    # print(result)

    query = '((rate(node_network_transmit_bytes_total[1m]) * 8) / (1000 * 1024 * 1024)) * 100'

    # query = '100 * (sum(increase(network_bytes_sent{device="enps03"} [1m]))) / on (instance) sum(increase(node_network_transmit_bytes{device="enps03"} [1m]))'

    resp = p_connect.custom_query(query)

    # print(resp)

    for entry in resp:
        instance = entry['metric']['instance']
        device = entry['metric']['device']
        if 'localhost' not in instance and device == 'enp0s3':
            value = entry['value'][1]
            result[instance].append(value)

    print(result)

    vm1_values = {
        'cpu_load': result['127.0.1.1:9501'][0],
        'ram_usage': result['127.0.1.1:9501'][1],
        'network_usage': result['127.0.1.1:9501'][2]
    }

    vm2_values = {
        'cpu_load': result['127.0.1.1:9502'][0],
        'ram_usage': result['127.0.1.1:9502'][1],
        'network_usage': result['127.0.1.1:9502'][2]
    }

    # vm3_values = {
    #     'cpu_load': result['127.0.1.1:9503'][0],
    #     'ram_usage': result['127.0.1.1:9503'][1],
    #     'network_usage': result['127.0.1.1:9503'][2]
    # }

    # vm4_values = {
    #     'cpu_load': result['127.0.1.1:9504'][0],
    #     'ram_usage': result['127.0.1.1:9504'][1],
    #     'network_usage': result['127.0.1.1:9504'][2]
    # }

    alts = np.array([
        list(vm1_values.values()),
        list(vm2_values.values()),
        # list(vm3_values.values()),
        # list(vm4_values.values()),
    ], dtype='float')


    weights = np.array(wts)
    types = np.array([-1, 1, -1])

    promethee = PROMETHEE_II('usual')

    pref = promethee(alts, weights, types)

    pref = promethee(alts, weights, types)

    ranking = rrankdata(pref)

    return ranking[0]

print(GetRank())
