#!/usr/bin/env python3
import osmium
import json
import datetime as dt
from pathlib import Path

# Define tag filters for different service types
SCHOOL_TAGS = {
    "amenity": {"school", "kindergarten", "childcare", "college", "university"}
}
HEALTH_TAGS = {
    "amenity": {"pharmacy", "hospital", "clinic", "doctors", "dentist"},
    "healthcare": set()
}
FOOD_TAGS = {
    "shop": set(),
    "amenity": {"marketplace"}
}

class OSMServiceExtractor(osmium.SimpleHandler):
    def __init__(self):
        self.services = {
            "schools": [],  # list of (lat, lon)
            "health": [],
            "food": [],
        }
    
    def way(self, w):
        # Check if the way is a closed polygon (area)
        if not w.is_closed():
            return
            
        # Extract coordinates for center of the polygon
        lats = []
        lons = []
        for nd in w.nodes:
            if nd.location.valid():
                lats.append(nd.location.lat)
                lons.append(nd.location.lon)
        
        if not lats:
            return
            
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        
        # Check tags
        amenity = w.tags.get("amenity", "")
        healthcare = w.tags.get("healthcare", "")
        
        # Schools
        if amenity in SCHOOL_TAGS["amenity"]:
            self.services["schools"].append((center_lat, center_lon))
        
        # Health
        if amenity in HEALTH_TAGS["amenity"] or healthcare:
            self.services["health"].append((center_lat, center_lon))
        
        # Food (shops and markets)
        shop = w.tags.get("shop", "")
        if shop or amenity in FOOD_TAGS["amenity"]:
            self.services["food"].append((center_lat, center_lon))
    
    def node(self, n):
        # Also check nodes (single points)
        if not n.location.valid():
            return
            
        lat = n.location.lat
        lon = n.location.lon
        
        amenity = n.tags.get("amenity", "")
        healthcare = n.tags.get("healthcare", "")
        
        # Schools
        if amenity in SCHOOL_TAGS["amenity"]:
            self.services["schools"].append((lat, lon))
        
        # Health
        if amenity in HEALTH_TAGS["amenity"] or healthcare:
            self.services["health"].append((lat, lon))
        
        # Food (shops and markets)
        shop = n.tags.get("shop", "")
        if shop or amenity in FOOD_TAGS["amenity"]:
            self.services["food"].append((lat, lon))

def main():
    # Read OSM file
    osm_path = Path("data/otp/rete/torino_cintura.osm.pbf")
    extractor = OSMServiceExtractor()
    
    print(f"Processing {osm_path}...")
    extractor.apply_file(str(osm_path), locations=True)
    
    print(f"Found services:")
    for service_type, points in extractor.services.items():
        print(f"  {service_type}: {len(points)} locations")
    
    # Save to JSON
    output_path = Path("data/processed/servizi_osm_cintura.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert to the expected format for the existing accessibility script
    with open(output_path, "w") as f:
        json.dump({
            "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "avviso": "Servizi da OpenStreetMap nella cintura di Torino (fuori dal Comune di Torino). Fonte: OSM tramite pyosmium.",
            "servizi": {
                "scuole": [{
                    "lat": lat,
                    "lon": lon,
                    "fonte": "OSM"
                } for lat, lon in extractor.services["schools"]],
                "salute": [{
                    "lat": lat,
                    "lon": lon,
                    "fonte": "OSM"
                } for lat, lon in extractor.services["health"]],
                "cibo": [{
                    "lat": lat,
                    "lon": lon,
                    "fonte": "OSM"
                } for lat, lon in extractor.services["food"]]
            },
            "parametri": {
                "file_osm": str(osm_path),
                "confine_citta": "Comune di Torino (codice 1272) secondo le sezioni di censimento di ISTAT 2021"
            }
        }, f, ensure_ascii=False, indent=2)
    
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()