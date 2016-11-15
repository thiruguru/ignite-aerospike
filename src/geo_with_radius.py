from __future__ import print_function
import aerospike
from aerospike import GeoJSON
from aerospike import predicates as p
import pprint

config = { 'hosts': [ ('127.0.0.1', 3000)]}
client = aerospike.client(config).connect()

pp = pprint.PrettyPrinter(indent=2)

#client.index_geo2dsphere_create('test', 'pads', 'loc', 'pads_loc_geo')
#bins = {'pad_id': 1,
#        'loc': aerospike.geojson('{"type":"Point", "coordinates":[-80.604333, 28.608389]}')}
#client.put(('test', 'pads', 'launchpad1'), bins)

query = client.query('locality', 'location')
query.select('store','seller','address','loc')
query.where(p.geo_within_radius('loc', -94.2217082259192, 36.3689382317293, 1000))
stores = []
sellers = []
def matched_names((key, metadata, bins)):
    pp.pprint(bins)
    stores.append(bins['store'])
    sellers.append(bins['seller'])

query.foreach(matched_names)
pp.pprint(stores[1])
pp.pprint(sellers)
#records = query.results()
client.close()
