"""
risk/network/graph
~~~~~~~~~~~~~~~~~~
"""

from collections import defaultdict
from typing import Any, Dict, List

import networkx as nx
import numpy as np
import pandas as pd


class NetworkGraph:
    """A class to represent a network graph and process its nodes and edges.

    The NetworkGraph class provides functionality to handle and manipulate a network graph,
    including managing domains, annotations, and node significance data. It also includes methods
    for transforming and mapping graph coordinates, as well as generating colors based on node
    significance.
    """

    def __init__(
        self,
        network: nx.Graph,
        top_annotations: pd.DataFrame,
        domains: pd.DataFrame,
        trimmed_domains: pd.DataFrame,
        node_label_to_node_id_map: Dict[str, Any],
        node_significance_sums: np.ndarray,
    ):
        """Initialize the NetworkGraph object.

        Args:
            network (nx.Graph): The network graph.
            top_annotations (pd.DataFrame): DataFrame containing annotations data for the network nodes.
            domains (pd.DataFrame): DataFrame containing domain data for the network nodes.
            trimmed_domains (pd.DataFrame): DataFrame containing trimmed domain data for the network nodes.
            node_label_to_node_id_map (Dict[str, Any]): A dictionary mapping node labels to their corresponding IDs.
            node_significance_sums (np.ndarray): Array containing the significant sums for the nodes.
        """
        self.top_annotations = top_annotations
        self.domain_id_to_node_ids_map = self._create_domain_id_to_node_ids_map(domains)
        self.domains = domains
        self.domain_id_to_domain_terms_map = self._create_domain_id_to_domain_terms_map(
            trimmed_domains
        )
        self.domain_id_to_domain_info_map = self._create_domain_id_to_domain_info_map(
            trimmed_domains
        )
        self.trimmed_domains = trimmed_domains
        self.node_significance_sums = node_significance_sums
        self.node_id_to_domain_ids_and_significance_map = (
            self._create_node_id_to_domain_ids_and_significances(domains)
        )
        self.node_id_to_node_label_map = {v: k for k, v in node_label_to_node_id_map.items()}
        self.node_label_to_significance_map = dict(
            zip(node_label_to_node_id_map.keys(), node_significance_sums)
        )
        self.node_label_to_node_id_map = node_label_to_node_id_map
        # NOTE: Below this point, instance attributes (i.e., self) will be used!
        self.domain_id_to_node_labels_map = self._create_domain_id_to_node_labels_map()
        # Unfold the network's 3D coordinates to 2D and extract node coordinates
        self.network = _unfold_sphere_to_plane(network)
        self.node_coordinates = _extract_node_coordinates(self.network)

    @staticmethod
    def _create_domain_id_to_node_ids_map(domains: pd.DataFrame) -> Dict[int, Any]:
        """Create a mapping from domains to the list of node IDs belonging to each domain.

        Args:
            domains (pd.DataFrame): DataFrame containing domain information, including the 'primary domain' for each node.

        Returns:
            Dict[int, Any]: A dictionary where keys are domain IDs and values are lists of node IDs belonging to each domain.
        """
        cleaned_domains_matrix = domains.reset_index()[["index", "primary_domain"]]
        node_to_domains_map = cleaned_domains_matrix.set_index("index")["primary_domain"].to_dict()
        domain_id_to_node_ids_map = defaultdict(list)
        for k, v in node_to_domains_map.items():
            domain_id_to_node_ids_map[v].append(k)

        return domain_id_to_node_ids_map

    @staticmethod
    def _create_domain_id_to_domain_terms_map(trimmed_domains: pd.DataFrame) -> Dict[int, Any]:
        """Create a mapping from domain IDs to their corresponding terms.

        Args:
            trimmed_domains (pd.DataFrame): DataFrame containing domain IDs and their corresponding labels.

        Returns:
            Dict[int, Any]: A dictionary mapping domain IDs to their corresponding terms.
        """
        return dict(
            zip(
                trimmed_domains.index,
                trimmed_domains["normalized_description"],
            )
        )

    @staticmethod
    def _create_domain_id_to_domain_info_map(
        trimmed_domains: pd.DataFrame,
    ) -> Dict[int, Dict[str, Any]]:
        """Create a mapping from domain IDs to their corresponding full description and significance score.

        Args:
            trimmed_domains (pd.DataFrame): DataFrame containing domain IDs, full descriptions, and significance scores.

        Returns:
            Dict[int, Dict[str, Any]]: A dictionary mapping domain IDs (int) to a dictionary with 'full_descriptions' and 'significance_scores'.
        """
        return {
            int(id_): {
                "full_descriptions": trimmed_domains.at[id_, "full_descriptions"],
                "significance_scores": trimmed_domains.at[id_, "significance_scores"],
            }
            for id_ in trimmed_domains.index
        }

    @staticmethod
    def _create_node_id_to_domain_ids_and_significances(domains: pd.DataFrame) -> Dict[int, Dict]:
        """Creates a dictionary mapping each node ID to its corresponding domain IDs and significance values.

        Args:
            domains (pd.DataFrame): A DataFrame containing domain information for each node. Assumes the last
                two columns are 'all domains' and 'primary domain', which are excluded from processing.

        Returns:
            Dict[int, Dict]: A dictionary where the key is the node ID (index of the DataFrame), and the value is another dictionary
                with 'domain' (a list of domain IDs with non-zero significance) and 'significance'
                (a dict of domain IDs and their corresponding significance values).
        """
        # Initialize an empty dictionary to store the result
        node_id_to_domain_ids_and_significances = {}
        # Get the list of domain columns (excluding 'all domains' and 'primary domain')
        domain_columns = domains.columns[
            :-2
        ]  # The last two columns are 'all domains' and 'primary domain'
        # Iterate over each row in the dataframe
        for idx, row in domains.iterrows():
            # Get the domains (column names) where the significance score is greater than 0
            all_domains = domain_columns[row[domain_columns] > 0].tolist()
            # Get the significance values for those domains
            significance_values = row[all_domains].to_dict()
            # Store the result in the dictionary with index as the key
            node_id_to_domain_ids_and_significances[idx] = {
                "domains": all_domains,  # The column names where significance > 0
                "significances": significance_values,  # The actual significance values for those columns
            }

        return node_id_to_domain_ids_and_significances

    def _create_domain_id_to_node_labels_map(self) -> Dict[int, List[str]]:
        """Create a map from domain IDs to node labels.

        Returns:
            Dict[int, List[str]]: A dictionary mapping domain IDs to the corresponding node labels.
        """
        domain_id_to_label_map = {}
        for domain_id, node_ids in self.domain_id_to_node_ids_map.items():
            domain_id_to_label_map[domain_id] = [
                self.node_id_to_node_label_map[node_id] for node_id in node_ids
            ]

        return domain_id_to_label_map


def _unfold_sphere_to_plane(G: nx.Graph) -> nx.Graph:
    """Convert 3D coordinates to 2D by unfolding a sphere to a plane.

    Args:
        G (nx.Graph): A network graph with 3D coordinates. Each node should have 'x', 'y', and 'z' attributes.

    Returns:
        nx.Graph: The network graph with updated 2D coordinates (only 'x' and 'y').
    """
    for node in G.nodes():
        if "z" in G.nodes[node]:
            # Extract 3D coordinates
            x, y, z = G.nodes[node]["x"], G.nodes[node]["y"], G.nodes[node]["z"]
            # Calculate spherical coordinates theta and phi from Cartesian coordinates
            r = np.sqrt(x**2 + y**2 + z**2)
            theta = np.arctan2(y, x)
            phi = np.arccos(z / r)

            # Convert spherical coordinates to 2D plane coordinates
            unfolded_x = (theta + np.pi) / (2 * np.pi)  # Shift and normalize theta to [0, 1]
            unfolded_x = unfolded_x + 0.5 if unfolded_x < 0.5 else unfolded_x - 0.5
            unfolded_y = (np.pi - phi) / np.pi  # Reflect phi and normalize to [0, 1]
            # Update network node attributes
            G.nodes[node]["x"] = unfolded_x
            G.nodes[node]["y"] = -unfolded_y
            # Remove the 'z' coordinate as it's no longer needed
            del G.nodes[node]["z"]

    return G


def _extract_node_coordinates(G: nx.Graph) -> np.ndarray:
    """Extract 2D coordinates of nodes from the graph.

    Args:
        G (nx.Graph): The network graph with node coordinates.

    Returns:
        np.ndarray: Array of node coordinates with shape (num_nodes, 2).
    """
    # Extract x and y coordinates from graph nodes
    x_coords = dict(G.nodes.data("x"))
    y_coords = dict(G.nodes.data("y"))
    coordinates_dicts = [x_coords, y_coords]
    # Combine x and y coordinates into a single array
    node_positions = {
        node: np.array([coords[node] for coords in coordinates_dicts]) for node in x_coords
    }
    node_coordinates = np.vstack(list(node_positions.values()))
    return node_coordinates
