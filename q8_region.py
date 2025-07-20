# Copy location in "locations.txt"
# copy regions in  "franchisee.txt


import csv
from typing import List, Tuple
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt
def parse_franchisee_file(file_path: str) -> List[Tuple[str, Polygon]]:
    """Parse franchisee.txt file with format: region_number followed by city [lat,lng] lines"""
    franchisees = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_id = None
        coords = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a region number
            if line.isdigit():
                # If we have collected coordinates for a previous ID, create a polygon
                if current_id is not None and coords:
                    polygon = create_region_from_coordinates(coords)
                    franchisees.append((current_id, polygon))
                
                # Start a new region
                current_id = line
                coords = []
            else:
                # Parse coordinate line in format "City Name [lat,lng]"
                if '[' in line and ']' in line:
                    try:
                        # Extract coordinates from brackets
                        coords_str = line[line.find('[') + 1:line.find(']')]
                        lat_str, lng_str = coords_str.split(',')
                        lat = float(lat_str.strip())
                        lng = float(lng_str.strip())
                        coords.append((lat, lng))
                    except (ValueError, IndexError) as e:
                        print(f"Warning: Invalid coordinate '{line}' - {e}")
                else:
                    print(f"Warning: Invalid coordinate format '{line}' - no brackets found")
        
        # Handle the last region after the loop ends
        if current_id is not None and coords:
            polygon = create_region_from_coordinates(coords)
            franchisees.append((current_id, polygon))
    print(f"Parsed {len(franchisees)} franchisee regions from {file_path}")
    return franchisees

def create_region_from_coordinates(coords: List[Tuple[float, float]]) -> Polygon:
    shapely_coords = [(lon, lat) for lat, lon in coords]
    return Polygon(shapely_coords)


def is_point_in_region(point: Tuple[float, float], region: Polygon) -> bool:
    """
    Check if a point is inside a given polygon region.
    Args:
        point: A tuple of (latitude, longitude)
        region: A Shapely Polygon representing the region   
    Returns:
        True if the point is inside the region, False otherwise
    """
    lat, lon = point
    shapely_point = Point(lon, lat)
    return region.contains(shapely_point)

# check if point on the edge of the polygon
def is_point_on_edge(point: Tuple[float, float], region: Polygon) -> bool:
    """
    Check if a point is on the edge of a given polygon region.
    
    Args:
        point: A tuple of (latitude, longitude)
        region: A Shapely Polygon representing the region
        
    Returns:
        True if the point is on the edge of the region, False otherwise
    """
    lat, lon = point
    shapely_point = Point(lon, lat)
    return region.touches(shapely_point)


def parse_locations(loc_path: str) -> List[Tuple[float, float]]:
    locations = []
    with open(loc_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue
                
            # Try different delimiters - tabs first, then commas, then spaces
            if '\t' in line:
                parts = line.split('\t')
            elif ',' in line:
                parts = line.split(',')
            else:
                parts = line.split()
            
            if len(parts) >= 2:
                try:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    locations.append((lat, lon))
                except ValueError as e:
                    print(f"Warning: Invalid coordinates on line {line_num}: '{line}' - {e}")
            else:
                print(f"Warning: Line {line_num} doesn't have enough coordinates: '{line}'")
    print(f"Parsed {len(locations)} locations from {loc_path}")
    return locations

def main():
    fr_path = 'franchisee.txt'
    loc_path = 'Locations.txt'

    # Parse the locations file
    loc = parse_locations(loc_path)

    # Parse the franchisee file
    franchisees = parse_franchisee_file(fr_path)

    # check each loc is inside which franchisee region
    for loc_point in loc:
        print(f"Checking location {loc_point} against franchisee regions:")
        for franchisee_id, region in franchisees:
            if is_point_in_region(loc_point, region):
                print(f"Location {loc_point} is inside franchisee {franchisee_id}")
            elif is_point_on_edge(loc_point, region):
                print(f"Location {loc_point} is on the edge of franchisee {franchisee_id}")

if __name__ == "__main__":
    main()

