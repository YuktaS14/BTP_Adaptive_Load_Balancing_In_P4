from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI


from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI

# controller = SimpleSwitchP4RuntimeAPI(device_id=1, grpc_port=9559,
#                                       p4rt_path='fd_p4rt.txt',
#                                       json_path='fd.json')

# controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["2"], ["10.0.0.1", "00:00:0a:00:00:01", "00:01:0a:00:00:01"])
# controller.table_add("MyIngress.get_addr","MyIngress.change_dst", ["3"], ["10.0.0.2", "00:00:0a:00:00:02", "00:01:0a:00:00:02"])
# controller.table_add("MyIngress.if_info","MyIngress.set_if_info", ["1"], ["0"])
# controller.table_add("MyIngress.if_info","MyIngress.set_if_info", ["2"], ["1"])
# controller.table_add("MyIngress.if_info","MyIngress.set_if_info", ["3"], ["1"])



# table_add MyIngress.get_addr MyIngress.change_dst 2 => 10.0.0.1 00:00:0a:00:00:01 00:01:0a:00:00:01 
# table_add MyIngress.get_addr MyIngress.change_dst 3 => 10.0.0.2 00:00:0a:00:00:02 00:01:0a:00:00:02
# table_add MyIngress.if_info MyIngress.set_if_info 1 => 0
# table_add MyIngress.if_info MyIngress.set_if_info 2 => 1
# table_add MyIngress.if_info MyIngress.set_if_info 3 => 1

controller1 = SimpleSwitchThriftAPI(9090)

controller1.register_write('min_utilized',0, 2)

# pkt = controller.client.get_stream_packet('packet', timeout=30);
# print(put)


# num = int(input("Enter value 2 or 3 = "))

# controller1.register_write('min_utilized',0, int(num))

# CLIENT = controller.client.stream_in_q.get()

# print(CLIENT.get_p4info())

# controller.client

# pkt = CLIENT.get_stream_packet(type_='mac', timeout=15)
# print(pkt)


# num = 2;

# while True:

#     controller.register_write('min_utilized',0, int(num))