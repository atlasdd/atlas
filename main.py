import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import networkx as nx
import plotly.graph_objects as go
import random

app = dash.Dash(__name__)

attack_categories = {
    "Evasion Attacks": ["Bypassing Cylance AI", "Deep Learning Malware Evasion", "Facial Recognition Spoofing"],
    "Data Poisoning": ["Tay Poisoning", "VirusTotal Poisoning", "ClearviewAI Misconfiguration"],
    "Model Theft": ["GPT-2 Model Replication", "Microsoft Azure Service Evasion"],
    "Adversarial Examples": ["MITRE Physical Face Attack", "Microsoft Edge AI Evasion"],
}

G = nx.DiGraph()
for category, attacks in attack_categories.items():
    G.add_node(category, color='red', size=25)
    for attack in attacks:
        G.add_node(attack, color='blue', size=15)
        G.add_edge(category, attack)

pos = nx.spring_layout(G, seed=42)
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='gray'),
    mode='lines'
)
node_x = []
node_y = []
node_color = []
node_size = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_color.append(G.nodes[node]['color'])
    node_size.append(G.nodes[node]['size'])
node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    marker=dict(size=node_size, color=node_color, line=dict(width=2)),
    text=list(G.nodes()),
    textposition='top center'
)

app.layout = html.Div([
    html.H1("ATLAS - Adversarial ML Threat Matrix"),
    html.P("Interactive visualization of adversarial machine learning attack pathways."),
    dcc.Graph(id='network-graph', figure={
        'data': [edge_trace, node_trace],
        'layout': go.Layout(showlegend=False, hovermode='closest', margin=dict(b=0, l=0, r=0, t=40))
    })
])

if __name__ == '__main__':
    app.run_server(debug=True)
