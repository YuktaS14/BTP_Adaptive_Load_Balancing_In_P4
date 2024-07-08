interfaces:
	chmod +x ./../bin/veth_setup.sh
	./../bin/veth_setup.sh

compile:
	p4c --target bmv2 \
	    --arch v1model \
	    --p4runtime-files fd.p4info.txt \
	    fd.p4

runswitch:
	simple_switch_grpc -i 1@veth0 -i 2@veth2 -i 3@veth4 -i 4@veth6 -i 5@veth8 --pcap=./pcap --thrift-port 5000 --nanolog ipc:///tmp/bm-1-log.ipc --device-id 1 ./fd.json -- --grpc-server-addr 0.0.0.0:9559

startController:
	sudo python3 Controller.py

compileh:
	p4c --target bmv2 \
	    --arch v1model \
	    --p4runtime-files rr.p4info.txt \
	    rr.p4

runswitchh:
	simple_switch_grpc -i 1@veth0 -i 2@veth2 -i 3@veth4 -i 4@veth6 -i 5@veth8 --pcap=./pcap --thrift-port 5000 --nanolog ipc:///tmp/bm-1-log.ipc --log-console --device-id 1 ./rr.json -- --grpc-server-addr 0.0.0.0:9559


# loadp4prog:
# /

# terminals:
# 	../bin/create-terminal-windows.sh port1-veth3 port2-veth5 port3-veth7 port4-veth9

arp:
	sudo arp -s 10.0.0.4 52:54:00:07:26:35

clean:
	/bin/rm \
	fd.json \
	fd.p4i \
	fd.p4info.txt \
	ss-log.txt
del:
	chmod +x ./../bin/del_veth.sh
	./../bin/del_veth.sh