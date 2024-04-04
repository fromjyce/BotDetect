from scapy.all import rdpcap, IP
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from collections import defaultdict
from graph_tool.all import Graph

class DataBootstrap:
    def __init__(self, pcap_file):
        self.pcap_file = pcap_file

    def pcap_to_parquet(self, pcap_file):
        packets = rdpcap(pcap_file)
        data = []
        for packet in packets:
            if IP in packet:
                time = packet.time
                source = packet[IP].src
                destination = packet[IP].dst
                protocol = packet[IP].proto
                length = len(packet)
                info = packet.summary()
                data.append([time, source, destination, protocol, length, info])
        df = pd.DataFrame(data, columns=['time', 'source', 'destination', 'protocol', 'length', 'info'])
        parquet_file = "dummy.parquet"
        table = pa.Table.from_pandas(df)
        pq.write_table(table, parquet_file)
        return df, parquet_file

    def extract_flow_data(self, pq_file):
        flow_df = pd.read_parquet(pq_file)
        flow_data = []
        for index, row in flow_df.iterrows():
            if 'IP' in row['info']:
                sip = row['source']
                dip = row['destination']
                srcpkts = 1
                dstpkts = 0
                flow_data.append((sip, dip, srcpkts, dstpkts))
        return flow_data

    def flow_ingestion(self, flow_data):
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
        return aggregated_flows



    def build_graph(self, aggregated_flows):
        g = Graph(directed=True)

        edge_weight1 = g.new_edge_property("float")
        edge_weight2 = g.new_edge_property("float")

        srcpkts = g.new_edge_property("float")
        dstpkts = g.new_edge_property("float")

        vertex_map = {}
        for (v1, v2), data in aggregated_flows.items():
            weight1 = data['srcpkts']
            weight2 = data['dstpkts']

            if v1 not in vertex_map:
                vertex_map[v1] = g.add_vertex()
            if v2 not in vertex_map:
                vertex_map[v2] = g.add_vertex()

            v1_index = vertex_map[v1]
            v2_index = vertex_map[v2]

            if weight1 > 0:
                e1 = g.add_edge(v1_index, v2_index)
                edge_weight1[e1] = weight1
                srcpkts[e1] = weight1
            if weight2 > 0:
                e2 = g.add_edge(v2_index, v1_index)
                edge_weight2[e2] = weight2
                dstpkts[e2] = weight2

        g.edge_properties["srcpkts"] = srcpkts
        g.edge_properties["dstpkts"] = dstpkts

        return g


    
    def run(self):
        self.df, self.parquet_file = self.pcap_to_parquet(self.pcap_file)
        self.flow_data = self.extract_flow_data(self.parquet_file)
        self.aggregated_flow_data = self.flow_ingestion(self.flow_data)
        self.graph = self.build_graph(self.aggregated_flow_data)
        return self.df, self.graph