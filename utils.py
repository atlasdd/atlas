import json
import networkx as nx

def save_graph_to_json(graph, filename="threat_matrix.json"):
    data = {
        "nodes": [],
        "edges": []
    }
    for node in graph.nodes(data=True):
        data["nodes"].append({"id": node[0], "attributes": node[1]})
    for edge in graph.edges():
        data["edges"].append({"source": edge[0], "target": edge[1]})
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_graph_from_json(filename="threat_matrix.json"):
    with open(filename, "r") as f:
        data = json.load(f)
    graph = nx.DiGraph()
    for node in data["nodes"]:
        graph.add_node(node["id"], **node["attributes"])
    for edge in data["edges"]:
        graph.add_edge(edge["source"], edge["target"])
    return graph

def print_graph_info(graph):
    print("Nodes:")
    for node in graph.nodes(data=True):
        print(node)
    print("\nEdges:")
    for edge in graph.edges():
        print(edge)

if __name__ == "__main__":
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
    
    save_graph_to_json(G)
    loaded_graph = load_graph_from_json()
    print_graph_info(loaded_graph)
