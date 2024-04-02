from scapy.all import rdpcap,IP
from scapy.all import *
from collections import defaultdict
import os

os.makedirs("assets", exist_ok=True)

def flow_ingestion(flow_data):
    aggregated_flows = defaultdict(lambda: {'srcpkts': 0, 'dstpkts': 0})

    for flow in flow_data:
        sip, dip, srcpkts, dstpkts = flow
        key = (sip, dip)
        reverse = (dip, sip)
        if key in aggregated_flows:
            aggregated_flows[key]['srcpkts'] += srcpkts
            aggregated_flows[key]['dstpkts'] += dstpkts
        elif reverse in aggregated_flows:
            aggregated_flows[reverse]['srcpkts'] += dstpkts
            aggregated_flows[reverse]['dstpkts'] += srcpkts
        else:
            aggregated_flows[key] = {'srcpkts': srcpkts, 'dstpkts': dstpkts}
    return [(sip, dip, data['srcpkts'], data['dstpkts']) for (sip, dip), data in aggregated_flows.items()]

def extract_flow_data(packets):
    flow_data = []
    for pkt in packets:
        if IP in pkt:
            sip = pkt[IP].src
            dip = pkt[IP].dst
            srcpkts = 1
            dstpkts = 0
            flow_data.append((sip, dip, srcpkts, dstpkts))
    return flow_data

pcap_file = "path-to-file.pcap"
packets = rdpcap(pcap_file)

flow_data = extract_flow_data(packets)

aggregated_flows = flow_ingestion(flow_data)


print(aggregated_flows)
