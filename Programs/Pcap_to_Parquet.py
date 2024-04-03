from scapy.all import *
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def pcap_to_dataframe(pcap_file):
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
    return df

def dataframe_to_parquet(df, parquet_file):
    table = pa.Table.from_pandas(df)
    pq.write_table(table, parquet_file)

if __name__ == "__main__":
    pcap_file = "your_pcap_file.pcap"
    parquet_file = "output.parquet"
    df = pcap_to_dataframe(pcap_file)
    dataframe_to_parquet(df, parquet_file)
    print(f"Conversion completed. Parquet file saved as {parquet_file}")
