#variables
distance = 3000 #desired distance to buffer in meters
corr = 1.6 #correction parameter - no idea why, but it works
simpl_tolerance = 200 #tolerance for simplifying the buffered polygon to reduce number of nodes


##################################################################################
#https://gis.stackexchange.com/questions/254198/buffering-geojson-file-using-python
#use solution using GeoPandas, need to install using: pip3 install geopandas

import geopandas as gpd
from shapely.ops import polygonize

#Read the GeoJSON file
df = gpd.read_file('CZ.geojson')
df.head()

#https://stackoverflow.com/questions/72073417/userwarning-geometry-is-in-a-geographic-crs-results-from-buffer-are-likely-i
df.crs = "epsg:4326"
df = df.to_crs(crs=3857)

#buffer the polygon, but it creates outer polygon plus additional inner polygon
df.geometry = df.buffer(distance*corr)

#reduce number of polygon nodes
df.geometry= df.simplify(simpl_tolerance, preserve_topology=True)

#get rid of inner polygon, results in "type": "LineString"
df.geometry = df.geometry.exterior

#convert LineString back to Polygon
df.geometry = gpd.GeoSeries(polygonize(df.geometry))

#convert back to correct CRS
df = df.to_crs(crs=4326)

#save output
df.head()
df.to_file('CZbuffer.geojson')
