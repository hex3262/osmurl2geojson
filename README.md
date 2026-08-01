# OSRM Routing to uMap GeoJSON Converter

A lightweight Python script that converts an OpenStreetMap routing URL into a fully compliant GeoJSON file. It extracts both the **exact route track (line)** and **all individual waypoint marker pins**, bypassing common uMap data-import limitations.

## The Problem
When you export a route from `routing.openstreetmap.de` as a GPX file, it only contains the continuous track line. Your manually set start, intermediate, and destination waypoints are lost. Furthermore, pasting raw OSRM API URLs directly into uMap results in an `"Invalid data"` error due to nested response structures.

## The Solution
This tool fetches the official OSRM API data, restructures it into a standard `FeatureCollection`, and exports a file containing:
1. The exact continuous route track.
2. Individual, numbered map markers for every single waypoint.

---

## How to Use

### 1. Plan Your Route
1. Go to [routing.openstreetmap.de](https://openstreetmap.de) and create your route.
2. Select your transportation mode (Car, Bike, or Foot).
3. Copy the **entire URL** from your browser's address bar.

### 2. Convert to GeoJSON
Run the script from your terminal by passing the copied URL as an argument:

```bash
python3 osmurl2geojson "YOUR_COPIED_OSM_ROUTING_URL"
```

*Note: Always wrap the URL in double quotes `""` to prevent terminal errors with special characters like `&`.*

A new file named `umap_route.geojson` will be generated in your current directory.

### 3. Import into uMap
1. Open [uMap](https://openstreetmap.de) and click **Create a map** (or open an existing map in **Edit mode**).
2. Click the **Import data** icon (arrow pointing up) on the right sidebar (probably the second from above in the second group of icons).
3. Click **Browse** and select the generated `umap_route.geojson` file.
4. Set the format dropdown to **geojson** (may be recognized automatically).
5. Click **Import**.
6. Enjoy seeing your route in the overlay on top of the map.
7. You may modifiy the color and other attributes of the waypoints.
8. Save your map, if you want to keep it.

---

## Features
- **Zero Dependencies:** Uses only Python built-in standard libraries (`json`, `sys`, `urllib`).
- **Auto Profile Detection:** Automatically detects if your route was planned for a Car, Bike, or Foot passenger and requests the matching API profile.
- **Custom User-Agent:** Built-in header configuration to comply with OpenStreetMap server policies.

## License
This project is available under the [MIT License](LICENSE).
