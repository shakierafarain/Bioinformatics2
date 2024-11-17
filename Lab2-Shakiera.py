import streamlit as st
import pandas as pd
import networkx as nx
import requests
import matplotlib.pyplot as plt
from networkx.algorithms.centrality import (
    degree_centrality,
    betweenness_centrality,
    closeness_centrality,
    eigenvector_centrality,
)

# Function to retrieve PPI data from BioGRID (mockup for illustration)
def retrieve_ppi_biogrid(target_protein):
    # Placeholder for actual API request/response parsing logic
    data = {
        "ProteinA": ["P1", "P2", "P3"],
        "ProteinB": ["P4", "P5", "P6"],
        "InteractionType": ["binding", "regulation", "modification"],
    }
    df = pd.DataFrame(data)
    st.write("Fetched PPI data from BioGRID for protein:", target_protein)
    return df

# Function to retrieve PPI data from STRING (mockup for illustration)
def retrieve_ppi_string(target_protein):
    # Placeholder for actual API request/response parsing logic
    data = {
        "ProteinA": ["P7", "P8", "P9"],
        "ProteinB": ["P10", "P11", "P12"],
        "InteractionType": ["binding", "co-expression", "regulation"],
    }
    df = pd.DataFrame(data)
    st.write("Fetched PPI data from STRING for protein:", target_protein)
    return df

# Function to generate a network graph using NetworkX
def generate_network(dataframe):
    G = nx.Graph()
    for _, row in dataframe.iterrows():
        G.add_edge(row["ProteinA"], row["ProteinB"], interaction=row["InteractionType"])
    return G

# Function to calculate centralities
def get_centralities(network_graph):
    centralities = {
        "Degree Centrality": degree_centrality(network_graph),
        "Betweenness Centrality": betweenness_centrality(network_graph),
        "Closeness Centrality": closeness_centrality(network_graph),
        "Eigenvector Centrality": eigenvector_centrality(network_graph),
        "PageRank Centrality": nx.pagerank(network_graph),
    }
    return centralities

# Streamlit app interface
def main():
    st.title("Protein-Protein Interaction (PPI) Network Analysis")
    
    target_protein = st.text_input("Enter target protein ID:")
    database_choice = st.selectbox("Select database to retrieve PPI data:", ["BioGRID", "STRING"])
    
    if st.button("Retrieve and Analyze"):
        if database_choice == "BioGRID":
            ppi_data = retrieve_ppi_biogrid(target_protein)
        elif database_choice == "STRING":
            ppi_data = retrieve_ppi_string(target_protein)
        else:
            st.error("Invalid database selection.")
            return
        
        # Creating two columns as per the lab instructions
        col1, col2 = st.columns(2)

        # Column 1: PPI Data Information
        with col1:
            st.subheader("PPI Data Information")
            st.dataframe(ppi_data)
            st.write(f"Number of nodes: {ppi_data.ProteinA.nunique() + ppi_data.ProteinB.nunique()}")
            st.write(f"Number of edges: {len(ppi_data)}")

            # Generate network and plot it
            G = generate_network(ppi_data)
            plt.figure(figsize=(8, 6))
            nx.draw(G, with_labels=True, node_color='teal', node_size=1500, font_size=10)
            st.pyplot(plt)

        # Column 2: Centrality Measures
        with col2:
            st.subheader("Centrality Measures")
            centralities = get_centralities(G)
            for measure, values in centralities.items():
                st.write(f"**{measure}**")
                st.json(values)

if __name__ == "__main__":
    main()
