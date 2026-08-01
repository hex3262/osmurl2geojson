#!/usr/bin/env python3
"""OSRM to uMap GeoJSON Converter.

This script takes a routing URL e.g. from routing.openstreetmap.de,
fetches the precise track and waypoints via the OSRM API, and outputs
a standard-compliant GeoJSON file ready for import into uMap. This
makes it possible to make use of the additional display features
such as waypoints that uMap provides.
"""

import json
import sys
import urllib.parse
import urllib.request


def extract_coordinates(osm_url):
    """Parses the OpenStreetMap routing URL to extract coordinates and profile."""
    try:
        parsed_url = urllib.parse.urlparse(osm_url)
        params = urllib.parse.parse_qs(parsed_url.query)

        if "loc" not in params:
            raise ValueError("No locations ('loc=') found in the provided URL.")

        # Extract coordinates and swap from [lat, lon] to [lon, lat]
        swapped_locs = []
        for loc in params["loc"]:
            lat, lon = loc.split(",")
            swapped_locs.append(f"{lon.strip()},{lat.strip()}")

        # Auto-detect profile (car, bike, foot). Default to car.
        profile = "routed-car"
        if "srv" in params:
            srv_value = params["srv"][0]
            if srv_value == "1":
                profile = "routed-bike"
            elif srv_value == "2":
                profile = "routed-foot"

        return ";".join(swapped_locs), profile

    except ValueError as e:
        print(f"Error parsing URL: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main program expects exactly one argument."""
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <openstreetmap_routing_url>")
        sys.exit(1)

    coord_string, profile = extract_coordinates(sys.argv[1])
    profile = profile.replace("routed-", "")

    # Build the official OSRM API request URL
    api_url = \
f"http://router.project-osrm.org/route/v1/{profile}/{coord_string}?geometries=geojson&overview=full"

    try:
        print(f"Fetching data from OSRM API ({profile})...")
        req = urllib.request.Request(
            api_url, headers={"User-Agent": "OSRM-to-uMap-Converter/1.0"}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))

        if data.get("code") != "Ok":
            raise ValueError(f"API responded with an error code: {data.get('code')}")

        # Structure the final GeoJSON FeatureCollection
        umap_geojson = {"type": "FeatureCollection", "features": []}

        # Append the continuous route line
        route_feature = {
            "type": "Feature",
            "properties": {"name": "Route Track"},
            "geometry": data["routes"][0]["geometry"],
        }
        umap_geojson["features"].append(route_feature)

        # Append the specific waypoints as marker pins
        for index, wp in enumerate(data["waypoints"]):
            street_name = wp.get("name", "")
            wp_name = (
                f"Waypoint {index + 1} ({street_name})"
                if street_name
                else f"Waypoint {index + 1}"
            )

            wp_feature = {
                "type": "Feature",
                "properties": {"name": wp_name, "description": "OSRM Waypoint"},
                "geometry": {"type": "Point", "coordinates": wp["location"]},
            }
            umap_geojson["features"].append(wp_feature)

        # Export to file
        output_filename = "umap_route.geojson"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(umap_geojson, f, ensure_ascii=False, indent=2)

        print( \
f"Exported one route track and {len(data['waypoints'])} waypoints to '{output_filename}'.")

    except Exception as e:
        print(f"Error fetching or saving data: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
