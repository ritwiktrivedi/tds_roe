# NOTE:  Update required depends on given data format

import csv
import networkx as nx
from typing import List, Tuple, Dict
from haversine import haversine, Unit


def calculate_haversine_distance(coord1: Tuple[float, float], 
                                 coord2: Tuple[float, float]) -> float:
    return haversine(coord1, coord2, unit=Unit.KILOMETERS)


def create_flight_graph(cities: Dict[str, Tuple[float, float]], 
                       connections: List[Tuple[str, str]]) -> nx.Graph:
    graph = nx.Graph()
    
    # Add all cities as nodes
    for city_name in cities.keys():
        graph.add_node(city_name)
    
    # Add edges only for direct flight connections
    for from_city, to_city in connections:
        if from_city in cities and to_city in cities:
            distance = calculate_haversine_distance(cities[from_city], cities[to_city])
            graph.add_edge(from_city, to_city, weight=distance)
    
    return graph


def find_shortest_path(graph: nx.Graph, start: str, end: str) -> Tuple[List[str], float]:
    try:
        path = nx.shortest_path(graph, start, end, weight='weight')
        total_distance = nx.shortest_path_length(graph, start, end, weight='weight')
        return path, total_distance
    except nx.NetworkXNoPath:
        return [], float('inf')


def write_shortest_path_to_csv(path: List[str], filename: str):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(path)


def main():
    """
    Example usage of the shortest path finder.
    """
    # Example cities with coordinates (latitude, longitude)
    cities = {
        "New York": (40.7128, -74.0060),
        "London": (51.5074, -0.1278),
        "Paris": (48.8566, 2.3522),
        "Tokyo": (35.6762, 139.6503),
        "Sydney": (-33.8688, 151.2093),
        "Dubai": (25.2048, 55.2708)
    }
    
    # Example direct flight connections
    connections = [
        ("New York", "London"),
        ("London", "Paris"),
        ("Paris", "Dubai"),
        ("Dubai", "Tokyo"),
        ("Tokyo", "Sydney"),
        ("New York", "Dubai"),
        ("London", "Dubai")
    ]
    
    # Create the flight graph
    graph = create_flight_graph(cities, connections)
    
    # Find shortest path from New York to Sydney
    start_city = "New York"
    end_city = "Sydney"
    path, distance = find_shortest_path(graph, start_city, end_city)
    if path:
        write_shortest_path_to_csv(path, "shortest_path.csv")

if __name__ == "__main__":
    main()