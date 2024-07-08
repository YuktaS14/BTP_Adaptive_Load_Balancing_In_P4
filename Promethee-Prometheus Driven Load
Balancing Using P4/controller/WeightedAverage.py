

from NodeExtractor import LoadMetrics
from Ahp import weights


# print(weights.target_weights)
print('IN WtdAverage')

# print(weights.target_weights)

wts = list(weights.target_weights.values())


n = len(wts)
v1 = list(LoadMetrics.values())
v2 = [5*x for x in v1]
v3 = [10*x for x in v1]

l1 = l2 = l3 = 0
for i in range(n): 
    l1 = v1[i]*wts[i]
    l2 = v2[i]*wts[i]
    l3 = v3[i]*wts[i]   

Lavg = (l1+l2+l3)/3


print(l1)
print(l2)
print(l3)

N1 = round(Lavg/(0.5*l1 + 0.5*Lavg),4)
N2 = round(Lavg/(0.5*l2 + 0.5*Lavg),4)
N3 = round(Lavg/(0.5*l3 + 0.5*Lavg),4)


print(N1)
print(N2)
print(N3)

