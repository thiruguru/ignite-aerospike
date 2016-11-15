# import the module
from __future__ import print_function
import aerospike
from aerospike import GeoJSON
from aerospike import predicates as p
from geopy.geocoders import Nominatim

# Configure the client
config = { 'hosts': [ ('127.0.0.1', 3000)]}

loc_id=8
store=108
seller='xyz'
address = '300 SW 24th St, Bentonville, AR 72712'
zip='72712|xyz|108'

# Create a client and connect it to the cluster
try:
	client = aerospike.client(config).connect()
except:
  import sys
  print("failed to connect to the cluster with", config['hosts'])
  sys.exit(1)

# create an index for geojson
client.index_geo2dsphere_create('locality', 'location', 'loc', 'loc_geo')

#get the latitude and langitude from the given address

geolocator = Nominatim()
location = geolocator.geocode(address)
#print(location.address)

loc = GeoJSON({'type': "Point",
               'coordinates': [location.longitude, location.latitude]})

bins = {'loc_id': loc_id,
	'store': store,
        'seller': seller,        
	'address' :address,
	'loc': loc}

try:
  # Write a record
	client.put(('locality', 'location', zip), bins)
except Exception as e:
  import sys
  print("error: {0}".format(e), file=sys.stderr)

# Close the connection to the Aerospike cluster
client.close()
