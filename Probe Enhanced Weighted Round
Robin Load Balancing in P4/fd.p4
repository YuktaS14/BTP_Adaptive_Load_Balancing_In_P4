/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;
typedef bit<48> time_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header probe_t {
    bit<4>   id; 
    bit<4>  cpu_percent;
    bit<4>  memory_percent;
    bit<4>  link_util;
    // bit<20>  network_bytes_sent;
    // bit<20>  network_bytes_received;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header tcp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4>  dataOffset;
    bit<4>  res;
    bit<1>  cwr;
    bit<1>  ecn;
    bit<1>  urg;
    bit<1>  ack;
    bit<1>  psh;
    bit<1>  rst;
    bit<1>  syn;
    bit<1>  fin;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}

struct routing_metadata_t {
    
    // bit<32> dst_ipv4;
    // bit<32> nhop_ipv4;
    // bit<48>  dst_mac;
    // bit<48>  src_mac;
    // bit<9>   egress_port;

    // bit<8>  if_index;    
    // bit<48> if_mac_addr;
    bit<8>  is_int_if;
    bit<16> packet_hash;
}

const bit<8>  TYPE_TCP  = 6;


struct metadata {
    routing_metadata_t routing_metadata;
    bit <16> l4_payload_length;
}

struct headers {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
    tcp_t        tcp;
    probe_t      probe;
}

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }
    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            0x800: parse_ipv4;
            default: accept;
        }
    }
    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        meta.l4_payload_length = hdr.ipv4.totalLen - (((bit<16>)hdr.ipv4.ihl) * 4);
        transition select(hdr.ipv4.protocol) {
            42: parse_probe;
            6: parse_tcp;
            default: accept;
        }
    }
    state parse_tcp {
        packet.extract(hdr.tcp);
        transition accept;
    }
    state parse_probe {
        packet.extract(hdr.probe);
        transition accept;
    }
}

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

// register<bit<48>> (65536) flowId_to_mac;
register<bit<9>> (65536) flowId_to_port_assinged;
register<bit<1>> (65536) flowId_to_is_assinged;
register<time_t> (65536) flowId_to_last_updated;

//assuming: max 15 servers-vms
register<bit<1>> (16) has_failed;
register<time_t> (15) probe_last_updated;


// register<bit<9>>(1) min_utilized;

register<bit<8>>(1) cur_server_id;


register<bit<5>>(1) vm_conn_counter;

register<bit<8>>(1) no_of_vms;

register<bit<5>>(34) vm_weights;

// register<bit<3>>(4) ahp_weights;

// register<bit<24>>(1) tempV;

#define CPU 3
#define MEMORY 1
#define LINK_UTIL 6
#define TIME_THRESHOLD 50000000000000
#define PKT_INSTANCE_TYPE_INGRESS_CLONE 1
#define PROBE_TIMEOUT 10000000000



control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    action drop() {
        mark_to_drop(standard_metadata);
    }

    // action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
    //     standard_metadata.egress_spec = port;
    //     if(port == 1) // vm to client
    //     {
    //         hdr.ethernet.srcAddr = 0x00010a000003;
    //         hdr.ipv4.srcAddr = 0x0a000004;
    //         hdr.ipv4.dstAddr = 0x0a000003;
    //         hdr.ethernet.dstAddr = 0x00000a000003;
            
    //     }
    //     else{
    //         // hdr.ipv4.srcAddr = 0x0a000005;
    //         hdr.ethernet.srcAddr = 0x00010a000001;
    //         hdr.ethernet.dstAddr = 0x00000a000001;
    //         hdr.ipv4.dstAddr = 0x0a000001;
    //         // hdr.ethernet.dstAddr = dstAddr;
    //     }
    //     // hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    // }

    // table ipv4_lpm {
    //     key = {
    //         hdr.ipv4.dstAddr: lpm;
    //     }
    //     actions = {
    //         ipv4_forward;
    //         drop;
    //         NoAction;
    //     }
    //     size = 1024;
    //     default_action = drop();
    // }
    action change_dst(bit<32> dst_ipv4_addr, bit<48> dst_mac_addr, bit<48> switch_interface_mac){

        // hdr.ethernet.srcAddr = 0x00010a000002;
        hdr.ethernet.srcAddr = switch_interface_mac;
        hdr.ipv4.dstAddr = dst_ipv4_addr;
        hdr.ethernet.dstAddr = dst_mac_addr;

        // hdr.ipv4.srcAddr = 0x0a000004;                        
        // hdr.ethernet.srcAddr = 0x00010a000003;

    }
    
    table get_addr {
        actions = {change_dst; drop;}
        key = {  standard_metadata.egress_spec: exact; }
        size = 512;
    }  

    action set_if_info(bit<8> is_init){
        meta.routing_metadata.is_int_if = is_init;
    }

    table if_info {
        key = {
           standard_metadata.ingress_port: exact;
        }
        actions = {
           set_if_info;
           drop;
        }
        default_action = drop();        
    }

    action change_src(bit<32> src_ipv4_addr, bit<48> src_mac_addr, bit<32> dst_ipv4_addr, bit<48> dst_mac_addr){

        hdr.ipv4.srcAddr = src_ipv4_addr;
        hdr.ipv4.dstAddr = dst_ipv4_addr;
        hdr.ethernet.srcAddr = src_mac_addr;
        hdr.ethernet.dstAddr = dst_mac_addr;

    }
    
    table set_dst_addr {
        key = {  standard_metadata.egress_spec: exact; }
        actions = {change_src; drop;}
        size = 512;
    }

    action clone_packet(){
        const bit<32> REPORT_MIRROR_SESSION_ID = 500;
        clone(CloneType.I2E, REPORT_MIRROR_SESSION_ID);
    }

    apply {
        
        if (hdr.ipv4.isValid()) {

            hdr.ipv4.ttl = hdr.ipv4.ttl - 1;

            if_info.apply();

            //check if we should terminate and remove a flow entry
            if(hdr.tcp.isValid() && ((hdr.tcp.fin == 1 && hdr.tcp.ack == 1) || (hdr.tcp.rst == 1))){
                //terminate the connection

                // get the flowId => port set to 0, isAssigned = 0
                bit<16> flow_id;
                hash(flow_id, HashAlgorithm.csum16, (bit<16>)0, { hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, hdr.tcp.srcPort, hdr.tcp.dstPort, hdr.ipv4.protocol},(bit<16>)65535);
                

                // client->to vm
                if(standard_metadata.ingress_port == 1){
                    flowId_to_port_assinged.read(standard_metadata.egress_spec, (bit<32>) flow_id);
                }
                
                // vm -> client
                else{
                    standard_metadata.egress_spec = 1;
                    // set_dst_addr.apply();
                }


                flowId_to_is_assinged.write((bit<32>) flow_id, 0);
                flowId_to_port_assinged.write((bit<32>) flow_id, 0);

            }


            //dat pkt -Vm->client
            else if((meta.routing_metadata.is_int_if == 1) && ((bit<8>)hdr.ipv4.protocol != (bit<8>)42))   
            {
                //vm to clienti
                standard_metadata.egress_spec = 1;
                // set_dst_addr.apply();
            }
  
            // probe pkt        
            else if ((bit<8>)hdr.ipv4.protocol == (bit<8>)42){


                bit<5> wtd_mean = (bit<5>) ( ((bit<24>) ( (bit<24>) CPU*( (bit<24>) hdr.probe.cpu_percent)) +(bit<24>)  ((bit<24>) MEMORY*((bit<24>)hdr.probe.memory_percent)) + (bit<24>) ((bit<24>) LINK_UTIL*( (bit<24>) hdr.probe.link_util))) >> 3);

                vm_weights.write((bit<32>) hdr.probe.id, wtd_mean);

                time_t cur_time = standard_metadata.ingress_global_timestamp;
                probe_last_updated.write((bit<32>) hdr.probe.id, cur_time);
                has_failed.write((bit<32>) hdr.probe.id, 0);
            }

            // data pkt - client->vm
            else {

                // lb_logic.apply();
                bit<16> flow_id;
                hash(flow_id, HashAlgorithm.csum16, (bit<16>)0, { hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, hdr.tcp.srcPort, hdr.tcp.dstPort, hdr.ipv4.protocol},(bit<16>)65535);

                bit<1> flag;
                flowId_to_is_assinged.read(flag, (bit<32>) flow_id);

                // check new connection
                if(flag == 0 && hdr.tcp.syn == 1) { // new flow

                    bit<8> _cur_server_id;
                    bit<8> _no_of_vms;
                    bit<5> _vm_conn_counter; 
                
                    cur_server_id.read(_cur_server_id, (bit<32>) 0);
                    no_of_vms.read(_no_of_vms, (bit<32>) 0);
                    vm_conn_counter.read(_vm_conn_counter, (bit<32>)0);


                    //read the weight of current vm
                    bit<5> _vm_weight;
                    vm_weights.read(_vm_weight, (bit<32>) _cur_server_id);

                    if(_vm_weight <= 0 ) { 

                        _cur_server_id = _cur_server_id + 1;
                        cur_server_id.write((bit<32>) 0,_cur_server_id); 
                        vm_conn_counter.write((bit<32>)0, 0);

                        resubmit_preserving_field_list((bit<8>)1);
                    }

                    else{

                        //connitac
                        _vm_conn_counter = _vm_conn_counter + 1;
                        vm_conn_counter.write((bit<32>)0, _vm_conn_counter);
                        
                        
                        bit<1>check_failed;
                        has_failed.read(check_failed, (bit<32>) _cur_server_id);


                        time_t cur_time = standard_metadata.ingress_global_timestamp;    
                        time_t last_update_time;
                        probe_last_updated.read(last_update_time, (bit<32>) _cur_server_id);

                        if((cur_time-last_update_time) > PROBE_TIMEOUT){
                            has_failed.write((bit<32>)_cur_server_id, 1);
                            check_failed = 1;
                        }

                        if(check_failed == 1){
                            //handle vm failed for mew connections
                            _cur_server_id = _cur_server_id + 1;
                            cur_server_id.write((bit<32>) 0,_cur_server_id); 
                            vm_conn_counter.write((bit<32>)0, 0);

                            resubmit_preserving_field_list((bit<8>)1);
                        }
                        
                        //assign port acc to selected server_id
                        standard_metadata.egress_spec = (bit<9>)_cur_server_id + 1;

                        flowId_to_is_assinged.write((bit<32>) flow_id, 1);
                        flowId_to_port_assinged.write((bit<32>) flow_id, (bit<9>) standard_metadata.egress_spec);

                        flowId_to_last_updated.write((bit<32>) flow_id, cur_time);

                        
                        // for next conn
                        if(_vm_conn_counter >= _vm_weight){
                            //check _cur_server_id != num_vms
                            _cur_server_id = _cur_server_id + 1;
                            _vm_conn_counter = 0;
                            vm_conn_counter.write((bit<32>)0, 0);
                        }

                        if(_cur_server_id >= _no_of_vms + 1) { // serverID - 1 to n
                            _cur_server_id = 1;
                            vm_conn_counter.write((bit<32>)0, 0);
                        }

                        cur_server_id.write((bit<32>) 0,_cur_server_id);
                    }      
                }

                else {  // means old connection

                    // what if probe for this assigned vm was missing?

                    // get the last updated timestamp for the flowid
                    // find the difference between current and last_updated and check if its > the threshold

                    time_t cur_time = standard_metadata.ingress_global_timestamp;

                    time_t last_time;
                    flowId_to_last_updated.read(last_time, (bit<32>) flow_id);

                    // if yes set the reset bit and terminate the connection (discard flow entry for that flow id)
                    if(cur_time - last_time > TIME_THRESHOLD) {

                        // if we send packet back to the client then how to terminate connection with virtual machine ?
                        
                        clone_packet();
                        hdr.tcp.rst = 1;
                        flowId_to_port_assinged.read(standard_metadata.egress_spec, (bit<32>) flow_id);

                        flowId_to_is_assinged.write((bit<32>) flow_id, 0);
                        flowId_to_port_assinged.write((bit<32>) flow_id, 0);

                    }
                    else {
                        
                        //else get the port already assigned and send the pkt forward
                        flowId_to_port_assinged.read(standard_metadata.egress_spec, (bit<32>) flow_id);

                        //check if the port is valid
                        bit<1>check_failed;
                        bit<16>vm_id;
                        vm_id = (bit<16>)(standard_metadata.egress_spec -1);

                        time_t last_update_time;
                        probe_last_updated.read(last_update_time, (bit<32>) vm_id);


                        has_failed.read(check_failed, (bit<32>) vm_id);
                        
                        if((cur_time-last_update_time) > PROBE_TIMEOUT){
                            has_failed.write((bit<32>)vm_id, 1);
                            check_failed = 1;
                        }

                        if(check_failed == 1){
                            //handle failed vm
                            //reset
                            //change egress spec
                            //remove connection
                        }
                        else{
                            flowId_to_last_updated.write((bit<32>) flow_id, cur_time);
                        }
                    }

                }

                // else{
                    get_addr.apply();
                // }
            }  
            // if(hdr.probe.isValid()){

            if(standard_metadata.egress_spec == 1) {
                set_dst_addr.apply();
            }

        }
            // ipv4_lpm.apply();
        // }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {  

        if(standard_metadata.instance_type == PKT_INSTANCE_TYPE_INGRESS_CLONE){
            
            //set reset bit 1
            hdr.tcp.rst = 1;

            //swap src, dst -> ip, mac, port
            bit<48>temp;
            temp = (bit<48>)hdr.ipv4.dstAddr;
            hdr.ipv4.dstAddr = hdr.ipv4.srcAddr;
            hdr.ipv4.srcAddr = (bit<32>)temp;


            temp = hdr.ethernet.dstAddr;
            hdr.ethernet.dstAddr = hdr.ethernet.srcAddr;
            hdr.ethernet.srcAddr = temp;


            temp = (bit<48>)hdr.tcp.dstPort;
            hdr.tcp.dstPort = hdr.tcp.srcPort;
            hdr.tcp.srcPort = (bit<16>)temp;


            //egress port 1
            standard_metadata.egress_spec = 1;
        }
    }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers  hdr, inout metadata meta) {
     apply {
        update_checksum(
        hdr.ipv4.isValid(),
            { hdr.ipv4.version,
              hdr.ipv4.ihl,
              hdr.ipv4.diffserv,
              hdr.ipv4.totalLen,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.srcAddr,
              hdr.ipv4.dstAddr },
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16);

        update_checksum_with_payload(
            hdr.tcp.isValid(),
            {   hdr.ipv4.srcAddr,
                hdr.ipv4.dstAddr,
                8w0,
                hdr.ipv4.protocol,
                meta.l4_payload_length,
                hdr.tcp.srcPort,
                hdr.tcp.dstPort,
                hdr.tcp.seqNo,
                hdr.tcp.ackNo,
                hdr.tcp.dataOffset,
                hdr.tcp.res,
                hdr.tcp.cwr,
                hdr.tcp.ecn,
                hdr.tcp.urg,
                hdr.tcp.ack,
                hdr.tcp.psh,
                hdr.tcp.rst,
                hdr.tcp.syn,
                hdr.tcp.fin,
                hdr.tcp.window,
                16w0,
                hdr.tcp.urgentPtr
            },
            hdr.tcp.checksum, 
            HashAlgorithm.csum16);

    }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
