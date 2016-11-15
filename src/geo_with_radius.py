from __future__ import print_function
import aerospike
from aerospike import GeoJSON
from aerospike import predicates as p

config = { 'hosts': [ ('127.0.0.1', 3000)]}
client = aerospike.client(config).connect()

query = client.query('locality', 'location')
query.select('store','seller','address', 'loc')
query.where(p.geo_within_radius('loc', -94.2217082259192, 36.3689382317293, 1000))
records = query.results()
print(records)
client.close()
