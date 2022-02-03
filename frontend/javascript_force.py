"""
==========
Javascript
==========

Example of writing JSON format graph data and using the D3 Javascript library
to produce an HTML/Javascript drawing.

You will need to download the following directory:

- https://github.com/networkx/networkx/tree/main/examples/external/force
"""
import json
import gzip
import shutil
import pandas as pd
import numpy as np
import flask
import networkx as nx

# G = nx.barbell_graph(6, 3)
# # this d3 example uses the name attribute for the mouse-hover value,
# # so add a name to each node
# for n in G:
#     G.nodes[n]["name"] = n
# # write json formatted data
# d = nx.json_graph.node_link_data(G)  # node-link format to serialize
dt_net_loc = '../../data/raw/ChG-Miner_miner-chem-gene.tsv.gz'
dt_net_tsv_loc = '../../data/interim/dt_net.tsv'

## The drug-target network from Biosnap
#http://snap.stanford.edu/biodata/datasets/10002/10002-ChG-Miner.html)
with gzip.open(dt_net_loc, 'rb') as f_in:
  with open(dt_net_tsv_loc, 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)

## Convert to a pandas df
dt_net_df = pd.read_csv(dt_net_tsv_loc, sep = '\t', header=0)
dt_net_df.rename(columns={'#Drug':'drug', 'Gene':'gene'}, inplace=True)

## Convert to networkx Graph object
G1 = nx.from_pandas_edgelist(dt_net_df, source = 'drug', target = 'gene')

# write json
json.dump(d, open("force/force.json", "w"))
print("Wrote node-link JSON data to force/force.json")

# Serve the file over http to allow for cross origin requests
app = flask.Flask(__name__, static_folder="force")

@app.route("/")
def static_proxy():
    return app.send_static_file("force.html")


print("\nGo to http://localhost:8000 to see the example\n")
app.run(port=8000)
