from graph_tool import centrality as gt_centrality
from graph_tool.all import *
from graph_tool import topology
from graph_tool.centrality import pagerank as gt_pagerank
from graph_tool import stats as gt_stats
import pandas as pd


class GraphFeatures:
    def __init__(self, graph):
        self.graph = graph
    
    def calculate_properties(self, graph):
        properties = {
        'ID': graph.get_in_degrees(graph.get_vertices()),
        'OD': graph.get_out_degrees(graph.get_vertices()),
        'IDW': graph.edge_properties["srcpkts"].a,
        'ODW': graph.edge_properties["dstpkts"].a,
        'IDC': gt_pagerank(graph, weight=graph.edge_properties["srcpkts"]),
        'ODC': gt_pagerank(graph, weight=graph.edge_properties["dstpkts"]),
        'BC': gt_centrality.betweenness(graph)[0],  # Update this line
        'CC': gt_centrality.closeness(graph),
        'KC': gt_centrality.katz(graph),  # Update this line
        'PR': gt_centrality.pagerank(graph),  # Use pagerank function from centrality module
        'Hub': gt_centrality.hits(graph, weight=graph.edge_properties["srcpkts"])[0],
        'Authority': gt_centrality.hits(graph, weight=graph.edge_properties["dstpkts"])[1],
	'LCC': graph_tool.clustering.local_clustering(graph)
    }
        return properties
    
    def write_df(self, properties):
        vertex_indices = range(self.graph.num_vertices())
        data = {
            'Vertex': vertex_indices,
            'ID': [properties['ID'][v] for v in vertex_indices],
            'OD': [properties['OD'][v] for v in vertex_indices],
            'IDW': [properties['IDW'][v] if v in properties['IDW'] else 0 for v in vertex_indices],
            'ODW': [properties['ODW'][v] if v in properties['ODW'] else 0 for v in vertex_indices],
            'IDC': [properties['IDC'][v] if v in properties['IDC'] else 0 for v in vertex_indices],
            'ODC': [properties['ODC'][v] if v in properties['ODC'] else 0 for v in vertex_indices],
            'BC': [properties['BC'][v] if v in properties['BC'] else 0 for v in vertex_indices],
            'CC': [properties['CC'][v] if v in properties['CC'] else 0 for v in vertex_indices],
            'KC': [properties['KC'][v] if v in properties['KC'] else 0 for v in vertex_indices],
            'PR': [properties['PR'][v] if v in properties['PR'] else 0 for v in vertex_indices],
            'Hub': [properties['Hub'] for _ in vertex_indices],
            'Authority': [properties['Authority'][v] if v in properties['Authority'] else 0 for v in vertex_indices],
            'LCC': [properties['LCC'][v] if v in properties['LCC'] else 0 for v in vertex_indices],
        }
        df = pd.DataFrame(data)
        return df
    
    def run(self):
        self.properties = self.calculate_properties(self.graph)
        self.prop_df = self.write_df(self.properties)
        return self.prop_df