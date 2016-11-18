# import the module
from __future__ import print_function
import aerospike
import time

# Configure the client
config = {
  'hosts': [ ('127.0.0.1', 3000) ]
}

# Create a client and connect it to the cluster
try:
  client = aerospike.client(config).connect()
except:
  import sys
  print("failed to connect to the cluster with", config['hosts'])
  sys.exit(1)

# Records are addressable via a tuple of (namespace, set, key)
key = ('item_detail', 'price', '123456789|107')

try:
  # Write a record
  client.put(key, {'sellprice': 19.97,'upc':123456789,'store':107,'writeTime':int(time.time()*1000)})

except Exception as e:
  import sys
  print("error: {0}".format(e), file=sys.stderr)

# Close the connection to the Aerospike cluster
client.close()
