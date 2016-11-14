# import the module
from __future__ import print_function
import aerospike
from aerospike import GeoJSON
from aerospike import predicates as p
from geopy.geocoders import Nominatim

# Configure the client
config = { 'hosts': [ ('127.0.0.1', 3000)]}

# Create a client and connect it to the cluster
try:
	client = aerospike.client(config).connect()
except:
  import sys
  print("failed to connect to the cluster with", config['hosts'])
  sys.exit(1)

# create an index for geojson
client.index_geo2dsphere_create('ignite', 'location', 'zipsellerstore', 'loc_geo')

#get the latitude and langitude from the given address

geolocator = Nominatim()
location = geolocator.geocode("406 S Walton Blvd, Bentonville, AR 72712")
#print(location.address)

loc = GeoJSON({'type': "Point",
               'coordinates': [location.latitude, location.longitude]})

bins = {'loc_id': 1,
	'store_no':100,
	'address' :'406 S Walton Blvd, Bentonville, AR 72712',
        'loc': loc}

try:
  # Write a record
	client.put(('ignite', 'location', '72712|wm|100'), bins)
except Exception as e:
  import sys
  print("error: {0}".format(e), file=sys.stderr)

# Close the connection to the Aerospike cluster
client.close()
