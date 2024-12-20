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

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
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
    tcp_t      tcp;
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
            6: parse_tcp;
            default: accept;
        }
    }
    state parse_tcp {
        packet.extract(hdr.tcp);
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

register<bit<48>> (65536) flowId_to_mac;
register<bit<9>> (65536) flowId_to_port_assinged;
register<bit<1>> (65536) flowId_to_is_assinged;

register<bit<9>>(1) min_utilized;

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




    apply {
        if (hdr.ipv4.isValid()) {
            hdr.ipv4.ttl = hdr.ipv4.ttl - 1;

            // bit<9> x;

            // min_utilized.read(x, (bit<32>) 0);

            // if(x == 0) {
            //     min_utilized.write((bit<32>)0, (bit<9>) 4);
            // }

            if_info.apply();

            //vm to client
            if (meta.routing_metadata.is_int_if == 1){
                //dest-> client ip

                //get mac from ip of client??
                //calculate flowid
                //get mac from flow id

                hdr.ethernet.dstAddr = 0x00000a000003;
                hdr.ethernet.srcAddr = 0x00010a000003;
                hdr.ipv4.srcAddr = 0x0a000004;

                hdr.ipv4.dstAddr = 0x0a000003;

                standard_metadata.egress_spec = 1;



            }

            //client to vm
            else{
            // hdr.ipv4.srcAddr = 0x0a000005;
            // hdr.ethernet.srcAddr = 0x00010a000001;
            // hdr.ethernet.dstAddr = 0x00000a000001;
            // hdr.ipv4.dstAddr = 0x0a000001;
            // // hdr.ethernet.dstAddr = dstAddr;
               

            // check new connection

            bit<16> flow_id;

            hash(flow_id, HashAlgorithm.csum16, (bit<16>)0, { hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, hdr.tcp.srcPort, hdr.tcp.dstPort, hdr.ipv4.protocol},(bit<16>)65535);


            bit<1> flag;

            flowId_to_is_assinged.read(flag, (bit<32>) flow_id);

            if(flag == 0) { // new flow

            //flowid calculate


                //check if flowid present -> if yes get egress port and transfer to that traffic
                //else read port from min_utilized
                //store flow-id -> mac mapping
                //fstore low-id -> egress port

                min_utilized.read(standard_metadata.egress_spec, (bit<32>) 0);
                
                // if(standard_metadata.egress_spec == 2){
                //     min_utilized.write((bit<32>)0, (bit<9>) (3));
                // }
                // else{
                //     min_utilized.write((bit<32>)0, (bit<9>) (2));
                // }

                // get_addr.apply();

                flowId_to_is_assinged.write((bit<32>) flow_id, 1);
                flowId_to_port_assinged.write((bit<32>) flow_id, (bit<9>) standard_metadata.egress_spec);

            }

            else {  // means old connection
    
                flowId_to_port_assinged.read(standard_metadata.egress_spec, (bit<32>) flow_id);


            }

            get_addr.apply();

            }
            // ipv4_lpm.apply();
        }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {  }
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
