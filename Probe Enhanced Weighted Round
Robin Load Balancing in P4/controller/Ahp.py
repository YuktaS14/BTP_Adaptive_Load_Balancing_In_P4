import ahpy

from decimal import Decimal, getcontext 
  

# load_comparisons = {
#     ('cpu_load', 'memory_usage'): 4, ('cpu_load', 'network_usage'): 1/4, ('cpu_load', 'disk_io_usage'): 3, ('cpu_load', 'disk_space_usage'): 4,

#     ('ram_usage', 'cpu_load'): 1/4, ('ram_usage', 'network_usage'): 1/6, ('ram_usage', 'disk_io_usage'): 1/2, ('ram_usage', 'disk_space_usage'): 1,

#     ('network_usage', 'ram_usage'):6, ('network_usage', 'cpu_load'): 4, ('network_usage', 'disk_io_usage'): 5, ('network_usage', 'disk_space_usage'): 6,

#     ('disk_io_usage', 'ram_usage'): 2, ('disk_io_usage', 'network_usage'): 1/5, ('disk_io_usage', 'cpu_load'): 1/3, ('disk_io_usage', 'disk_space_usage'): 2,

#     ('disk_space_usage', 'ram_usage'): 1, ('disk_space_usage', 'network_usage'): 1/6, ('disk_space_usage', 'disk_io_usage'): 1/2, ('disk_space_usage', 'cpu_load'): 1/4,
# }





load_comparisons = {
    ('cpu_load', 'ram_usage'): 2, ('cpu_load', 'network_usage'): 1/3,

    ('ram_usage', 'cpu_load'): 1/2, ('ram_usage', 'network_usage'): 1/6, 

    ('network_usage', 'ram_usage'):6, ('network_usage', 'cpu_load'): 3, 
}


getcontext().prec = 3


weights = ahpy.Compare(name='Drinks', comparisons=load_comparisons, precision=6, random_index='saaty')

print(weights.target_weights)

print(list(weights.target_weights.values()))

print(weights.consistency_ratio)

ahp_wt = list(weights.target_weights.values())


#                   | cpu_load | ram_usage | network_usage | disk_io_usage | disk_space_usage
# -------------------------------------------------------------------------------------------
# cpu_load          |    1     |     3     |       7       |       5       |         5
# ram_usage         |   1/3    |     1     |       5       |       3       |         3
# network_usage     |  1/7    |   1/5    |       1       |       7       |         7
# disk_io_usage     |  1/5    |   1/3    |      1/7      |       1       |         5
# disk_space_usage  |  1/5    |   1/3    |      1/7      |      1/5      |         1
