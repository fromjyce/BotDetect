from scapy.all import rdpcap,IP
from scapy.all import *
from collections import defaultdict
from graph_tool.all import *
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

def build_graph(flow_data):
    g = Graph(directed=True)

    sip_prop = g.new_vertex_property("string")
    dip_prop = g.new_vertex_property("string")
    srcpkts_prop = g.new_edge_property("int")
    dstpkts_prop = g.new_edge_property("int")

    vertices = defaultdict(g.add_vertex)

    for sip, dip, srcpkts, dstpkts in flow_data:
        src_vertex = vertices[sip]
        dst_vertex = vertices[dip]
        edge = g.add_edge(src_vertex, dst_vertex)
        srcpkts_prop[edge] = srcpkts
        dstpkts_prop[edge] = dstpkts
        sip_prop[src_vertex] = sip
        dip_prop[dst_vertex] = dip

    g.vertex_properties["sip"] = sip_prop
    g.vertex_properties["dip"] = dip_prop
    g.edge_properties["srcpkts"] = srcpkts_prop
    g.edge_properties["dstpkts"] = dstpkts_prop

    return g

def draw_graph(graph, output_file):
    graph_draw(graph, vertex_text=graph.vertex_properties["sip"], output=output_file)


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


pcap_file = "file-to-path.pcap"
packets = rdpcap(pcap_file)


flow_data = extract_flow_data(packets)


aggregated_flows = flow_ingestion(flow_data)


print(aggregated_flows)

graph = build_graph(aggregated_flows)


graph_draw(graph, vertex_text=graph.vertex_index, output="assets/testscapy.png")
