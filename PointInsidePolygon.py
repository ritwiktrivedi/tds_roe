# Point inside polygon algorithm


def point_in_polygon(lat, lon, polygon):
    # Check if a point is inside a polygon using the ray-casting algorithm
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if lon > min(p1x, p2x):
            if lon <= max(p1x, p2x):
                if lat <= max(p1y, p2y):
                    if p1y != p2y:
                        xinters = (lon - p1x) * (p2y - p1y) / (p2x - p1x) + p1y
                    if p1y == p2y or lat <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def find_polygons_for_coordinates(coordinates, regions):
    results = []
    for lat, lon in coordinates:
        matching_polygons = []
        for region_name, polygon in regions.items():
            if point_in_polygon(lat, lon, polygon):
                matching_polygons.append(region_name)
        results.append(matching_polygons)
    return results
