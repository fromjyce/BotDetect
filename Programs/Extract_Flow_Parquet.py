import pandas as pd

def extract_flow_data(flow_df):
    flow_data = []
    for index, row in flow_df.iterrows():
        if 'IP' in row['info']:  # Assuming 'info' column contains protocol information
            sip = row['source']
            dip = row['destination']
            srcpkts = 1
            dstpkts = 0
            flow_data.append((sip, dip, srcpkts, dstpkts))
    return flow_data

# Load Parquet file
parquet_file = "output.parquet"
flow_df = pd.read_parquet(parquet_file)
