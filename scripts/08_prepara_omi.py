#!/usr/bin/env python3
"""
O1: Prepare OMI zones.
Reads the OMI quotations CSV and KML zone files,
generates data/processed/omi_zone.json with simplified polygons.
"""

import csv
import json
import math
import re
from pathlib import Path

def read_valori_csv(path):
    """Read QIP_1445919_1_20252_VALORI.csv and return list of rows.
    Skip the title row (first line) and use the second row as header."""
    with open(path, newline='', encoding='utf-8') as f:
        # Skip title row
        next(f)
        reader = csv.DictReader(f, delimiter=';')
        return list(reader)

def read_zone_csv(path):
    """Read QIP_1445919_1_20252_ZONE.csv and return list of rows.
    Skip the title row (first line) and use the second row as header."""
    with open(path, newline='', encoding='utf-8') as f:
        # Skip title row
        next(f)
        reader = csv.DictReader(f, delimiter=';')
        return list(reader)

def parse_kml_polygons(kml_dir):
    """
    Parse all KML files in the directory and return a dict:
    {(comune_amm, zona): [polygon_coords]}
    polygon_coords: list of (lon, lat) tuples for the outer boundary
    """
    polygons = {}
    
    for kml_path in kml_dir.glob('*.kml'):
        # Extract comune_amm from filename (e.g., L219.kml)
        comune_amm = kml_path.stem
        
        with open(kml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all Placemark elements
        # Each placemark has:
        # - <name>TORINO - Zona OMI D26</name>
        # - <ExtendedData><Data name="CODCOM"><value>L219</value></Data>...</ExtendedData>
        # - <Polygon><outerBoundaryIs><LinearRing><coordinates>...</coordinates></LinearRing></outerBoundaryIs></Polygon>
        
        # Split by Placemark tags
        placemark_sections = re.split(r'(?=<Placemark>)', content)
        
        for section in placemark_sections:
            if '<Placemark>' not in section:
                continue
                
            # Extract CODZONA
            codzona_match = re.search(r'<Data name="CODZONA">.*?<value>([^<]*)</value>', section, re.DOTALL)
            if not codzona_match:
                continue
            zona = codzona_match.group(1)
            
            # Verify CODCOM matches filename (should be L219 for Torino)
            codcom_match = re.search(r'<Data name="CODCOM">.*?<value>([^<]*)</value>', section, re.DOTALL)
            if not codcom_match:
                continue
            codcom = codcom_match.group(1)
            
            # Extract coordinates
            coords_match = re.search(r'<coordinates>(.*?)</coordinates>', section, re.DOTALL)
            if not coords_match:
                continue
                
            coords_str = coords_match.group(1).strip()
            # Parse coordinates: "lon1,lat1,0 lon2,lat2,0 ..."
            # We need to handle both spaces and newlines
            coords_str = coords_str.replace('\n', ' ').strip()
            # Split by spaces to get coordinate triplets
            coord_triplets = coords_str.split()
            
            # Build polygon (list of (lon, lat) tuples)
            polygon = []
            for triplet in coord_triplets:
                parts = triplet.split(',')
                if len(parts) >= 2:
                    try:
                        lon = float(parts[0])
                        lat = float(parts[1])
                        polygon.append((lon, lat))
                    except ValueError:
                        pass
            
            if polygon:
                key = (comune_amm, zona)
                if key not in polygons:
                    polygons[key] = []
                polygons[key].append(polygon)
    
    return polygons

def douglas_peucker(points, max_distance_meters=20.0):
    """
    Simplifies a polyline using Douglas-Peucker algorithm.
    Points are (lon, lat) tuples.
    max_distance_meters: maximum allowed distance between original and simplified curve.
    Returns a simplified list of points.
    """
    if len(points) <= 2:
        return points
    
    # Convert meters to approximate degrees at Torino latitude (~45°N)
    # 1 degree latitude ≈ 111.132 km
    # 1 degree longitude ≈ 111.132 * cos(lat) km
    # At 45°N: 1° lat ≈ 111.132 km, 1° lon ≈ 78.589 km
    # 20 meters = 0.02 km
    # Latitude degrees: 0.02 / 111.132 ≈ 0.00018
    # Longitude degrees: 0.02 / 78.589 ≈ 0.000254
    # We'll use the larger value to be safe: ~0.00025 degrees
    max_distance_deg = 0.00025  # approximately 20 meters at 45°N
    
    def distance(p1, p2):
        """Euclidean distance between two points (lon, lat) in degrees."""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def point_to_line_dist(point, line_start, line_end):
        """Distance from a point to a line segment."""
        x0, y0 = point
        x1, y1 = line_start
        x2, y2 = line_end
        
        # If line segment is a point
        if distance(line_start, line_end) < 1e-12:
            return distance(point, line_start)
        
        # Calculate the projection parameter t
        dx = x2 - x1
        dy = y2 - y1
        t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))
        
        # Closest point on the segment
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        
        return distance(point, (closest_x, closest_y))
    
    def is_within_tolerance(point, line_start, line_end, max_dist):
        """Check if a point is within max_dist of the line segment."""
        return point_to_line_dist(point, line_start, line_end) <= max_dist
    
    # Recursive Douglas-Peucker
    def simplify_recursive(points, start_idx, end_idx):
        if end_idx - start_idx <= 1:
            return [points[start_idx]]
        
        # Find the point with maximum distance from the line segment
        max_dist = 0
        max_idx = start_idx
        
        start_point = points[start_idx]
        end_point = points[end_idx]
        
        for i in range(start_idx + 1, end_idx):
            dist = point_to_line_dist(points[i], start_point, end_point)
            if dist > max_dist:
                max_dist = dist
                max_idx = i
        
        # If max distance is within tolerance, keep only endpoints
        if max_dist <= max_distance_deg:
            return [start_point, end_point]
        
        # Otherwise, split at the point of max distance and recurse
        left = simplify_recursive(points, start_idx, max_idx)
        right = simplify_recursive(points, max_idx, end_idx)
        
        # Combine (avoid duplicating the split point)
        return left[:-1] + right
    
    return simplify_recursive(points, 0, len(points) - 1)

def main():
    # Paths
    base_dir = Path("C:/projects/Progetti/GTT")
    raw_dir = base_dir / "data" / "raw"
    processed_dir = base_dir / "data" / "processed"
    
    # Read data
    valori_path = raw_dir / "QIP1445919_CMPLRD98T08F335C" / "QIP_1445919_1_20252_VALORI.csv"
    zone_path = raw_dir / "QIP1445919_CMPLRD98T08F335C" / "QIP_1445919_1_20252_ZONE.csv"
    kml_dir = raw_dir / "QIP1445919_CMPLRD98T08F335C" / "TO20252"
    
    if not valori_path.exists() or not zone_path.exists() or not kml_dir.exists():
        print(f"Error: Required files not found")
        print(f"  valori: {valori_path.exists()}")
        print(f"  zone: {zone_path.exists()}")
        print(f"  kml_dir: {kml_dir.exists()}")
        return
    
    print("Reading CSV files...")
    valori = read_valori_csv(valori_path)
    zones = read_zone_csv(zone_path)
    
    print(f"  Valori rows: {len(valori)}")
    print(f"  Zone rows: {len(zones)}")
    
    # Parse KML polygons
    print("Parsing KML files...")
    kml_polygons = parse_kml_polygons(kml_dir)
    print(f"  Found polygons for {len(kml_polygons)} (comune, zona) pairs")
    
    # Build mapping from zone code to zone name using ZONE.csv
    zone_name_map = {}  # (comune_amm, zona) -> zone_name
    for row in zones:
        key = (row['Comune_amm'], row['Zona'])
        zone_name_map[key] = row['Zona_Descr']
    
    # Group valori by (comune_amm, zona)
    valori_by_zone = {}  # (comune_amm, zona) -> list of valore rows
    for row in valori:
        key = (row['Comune_amm'], row['Zona'])
        if key not in valori_by_zone:
            valori_by_zone[key] = []
        valori_by_zone[key].append(row)
    
    # Build the output JSON structure
    output = []
    
    # Process each comune in the valori data
    # First collect (comune_amm, zona, row) samples for PRO_COM lookup
    comuni_amm = {}  # comune_amm -> row (first row seen for this comune)
    for row in valori:
        comune_amm = row['Comune_amm']
        if comune_amm not in comuni_amm:
            comuni_amm[comune_amm] = row
    
    print(f"Processing {len(comuni_amm)} comuni from valori data...")
    
    for comune_amm in sorted(comuni_amm):
        # Get PRO_COM code: Comune_ISTAT - 1000000
        sample_row = comuni_amm[comune_amm]
        pro_com = int(sample_row['Comune_ISTAT']) - 1000000
        
        # Build zone list for this comune
        zone_list = []
        
        # Get all zones for this comune from valori
        comune_zone_pairs = [(c, z) for (c, z) in valori_by_zone.keys() if c == comune_amm]
        
        for zona in sorted(set(z for (_, z) in comune_zone_pairs)):
            # Get zone name
            zone_name = zone_name_map.get((comune_amm, zona), zona)
            
            # Get fascia from first valore row for this (comune, zona)
            fascia = valori_by_zone[(comune_amm, zona)][0]['Fascia'] if (comune_amm, zona) in valori_by_zone else 'B'
            
            # Get polygons from KML
            polygon_key = (comune_amm, zona)
            raw_polygons = kml_polygons.get(polygon_key, [])
            
            # Apply Douglas-Peucker simplification to each polygon
            simplified_polygons = []
            for poly in raw_polygons:
                simplified = douglas_peucker(poly, max_distance_meters=20.0)
                # Convert from (lon, lat) to [lat, lon] as required
                lat_lon_pairs = [[lat, lon] for (lon, lat) in simplified]
                simplified_polygons.append(lat_lon_pairs)
            
            # Build valori dict: {cod_tipologia: [cmin, cmax, lmin, lmax]}
            valori_dict = {}
            for row in valori_by_zone.get((comune_amm, zona), []):
                cod_tip = row['Cod_Tip']
                # Convert comma decimal to point
                cmin = float(row['Compr_min'].replace(',', '.')) if row['Compr_min'] else 0.0
                cmax = float(row['Compr_max'].replace(',', '.')) if row['Compr_max'] else 0.0
                lmin = float(row['Loc_min'].replace(',', '.')) if row['Loc_min'] else 0.0
                lmax = float(row['Loc_max'].replace(',', '.')) if row['Loc_max'] else 0.0
                
                # Keep only NORMALE state if available, otherwise first
                if row['Stato'] == 'NORMALE':
                    valori_dict[cod_tip] = [cmin, cmax, lmin, lmax]
                    break  # Use first NORMALE
                elif cod_tip not in valori_dict:
                    valori_dict[cod_tip] = [cmin, cmax, lmin, lmax]
            
            # If no valori found, skip this zone (should not happen)
            if not valori_dict:
                continue
            
            zone_entry = {
                "z": zona,
                "n": zone_name,
                "f": fascia,
                "g": simplified_polygons,  # poligoni semplificati
                "v": valori_dict           # valori per tipologia
            }
            zone_list.append(zone_entry)
        
        if zone_list:
            comune_entry = {
                "c": pro_com,
                "zone": zone_list
            }
            output.append(comune_entry)
    
    # Write to file
    output_path = processed_dir / "omi_zone.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {output_path}")
    print(f"Total comuni processed: {len(output)}")
    
    # Verifica: stampa info su Torino
    torino_entry = next((c for c in output if c['c'] == 1272), None)
    if torino_entry:
        print(f"\nTorino (PRO_COM=1272):")
        print(f"  Zone count: {len(torino_entry['zone'])}")
        # Find zona B1
        b1_zone = next((z for z in torino_entry['zone'] if z['z'] == 'B1'), None)
        if b1_zone:
            print(f"  Zona B1 ({b1_zone['n']}):")
            print(f"    Fascia: {b1_zone['f']}")
            print(f"    Valori ab: {b1_zone['v'].get('20', [0,0,0,0])}")  # codice 20 = Abitazioni civili
            print(f"    Numero poligoni: {len(b1_zone['g'])}")
            if b1_zone['g']:
                print(f"    Primo anello punti: {len(b1_zone['g'][0])} coordinate")

if __name__ == "__main__":
    main()