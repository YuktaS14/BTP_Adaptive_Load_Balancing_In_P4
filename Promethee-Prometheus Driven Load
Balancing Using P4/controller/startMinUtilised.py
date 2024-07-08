from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI
import netifaces
import os
import time
from Promethee import GetRank

controller = SimpleSwitchThriftAPI(5000)

last  = -1

while True:

    min_utilized = GetRank()
    print('min_utilized = ' , min_utilized)

    if min_utilized != last:
        print('Chnaged min_utilized = ' , min_utilized)
        controller.register_write('min_utilized',0, min_utilized)
        last = min_utilized

    time.sleep(5)