from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI
import netifaces
import os
import time
from Promethee import GetRank

controller = SimpleSwitchThriftAPI(5000)

controller.table_add("MyIngress.if_info","MyIngress.set_if_info", ["1"], ["0"])
controller.table_add("MyIngress.if_info","MyIngress.set_if_info", ["2"], ["1"])
controller.table_add("MyIngress.if_info","MyIngress.set_if_info", ["3"], ["1"])
controller.table_add("MyIngress.if_info","MyIngress.set_if_info", ["4"], ["1"])
controller.table_add("MyIngress.if_info","MyIngress.set_if_info", ["5"], ["1"])


veth0 = netifaces.ifaddresses("veth0")[netifaces.AF_LINK][0]['addr']
veth2 = netifaces.ifaddresses("veth2")[netifaces.AF_LINK][0]['addr']
veth4 = netifaces.ifaddresses("veth4")[netifaces.AF_LINK][0]['addr']
veth6 = netifaces.ifaddresses("veth6")[netifaces.AF_LINK][0]['addr']
veth8 = netifaces.ifaddresses("veth8")[netifaces.AF_LINK][0]['addr']


# vm1 = "08:00:27:83:11:6a"
# controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["2"], ["10.0.0.11", vm1, veth2])

# vm2 = "08:00:27:b8:95:e3"
# controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["3"], ["10.0.0.12", vm2, veth4])

# vm3 = "08:00:27:20:46:b1"
# controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["4"], ["10.0.0.13", vm3, veth6])

# vm4 = "08:00:27:c2:55:e7"
# controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["5"], ["10.0.0.14", vm4, veth8])

vm1 = "08:00:27:2e:a9:e9"
controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["2"], ["10.0.0.11", vm1, veth2])
# controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["3"], ["10.0.0.3", veth4, veth5])

vm2 = "08:00:27:69:dc:ed"
controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["3"], ["10.0.0.12", vm2, veth4])

vm3 = "08:00:27:20:46:b1"
controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["4"], ["10.0.0.13", vm3, veth6])

vm4 = "08:00:27:c2:55:e7"
controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["5"], ["10.0.0.14", vm4, veth8])


veth0 = netifaces.ifaddresses("veth0")[netifaces.AF_LINK][0]['addr']
veth1 = netifaces.ifaddresses("veth1")[netifaces.AF_LINK][0]['addr']
controller.table_add("MyIngress.set_dst_addr","MyIngress.change_src", ["1"], ["10.0.0.52", veth0, "10.0.0.1", veth1])


command = "sudo arp -s 10.0.0.52 " + veth0;
os.system(command) 

last = -1
#
while True:

    min_utilized = GetRank()
    print('min_utilized = ' , min_utilized)

    if min_utilized != last:
        print('Chnaged min_utilized = ' , min_utilized)
        controller.register_write('min_utilized',0, min_utilized)
        last = min_utilized

    time.sleep(5)

'''
for mininet

vm1 = "00:00:0a:00:00:01"
s1_vm1 = "00:01:0a:00:00:01"

vm2 = "00:00:0a:00:00:02"
s1_vm2 = "00:01:0a:00:00:02"

c1 = "00:00:0a:00:00:03"
s1_c1 = "00:01:0a:00:00:03"

controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["2"], ["10.0.0.1", vm1, s1_vm1])
controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["3"], ["10.0.0.2", vm2, s1_vm2])


# controller.table_add("MyIngress.set_dst_addr","MyIngress.change_src", ["1"], ["10.0.0.4", s1_c1, "10.0.0.1", c1])
controller.table_add("MyIngress.set_dst_addr","MyIngress.change_src", ["1"], ["10.0.0.4", s1_c1, "10.0.0.3", c1])
'''
