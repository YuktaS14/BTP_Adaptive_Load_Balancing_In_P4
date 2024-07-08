import ahpy

load_comparisons = {
    ('cpu_load', 'ram_usage'): 4, ('cpu_load', 'network_usage'): 1/2,

    ('ram_usage', 'cpu_load'): 1/4, ('ram_usage', 'network_usage'): 1/6,

    ('network_usage', 'ram_usage'):6, ('network_usage', 'cpu_load'): 2
}

weights = ahpy.Compare(name='Drinks', comparisons=load_comparisons, precision=3, random_index='saaty')

print(weights.target_weights)

print(weights.consistency_ratio)


#                   | cpu_load | ram_usage | network_usage | disk_io_usage | disk_space_usage
# -------------------------------------------------------------------------------------------
# cpu_load          |    1     |     3     |       7       |       5       |         5
# ram_usage         |   1/3    |     1     |       5       |       3       |         3
# network_usage     |  1/7    |   1/5    |       1       |       7       |         7
# disk_io_usage     |  1/5    |   1/3    |      1/7      |       1       |         5
# disk_space_usage  |  1/5    |   1/3    |      1/7      |      1/5      |         1
