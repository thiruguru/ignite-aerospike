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
key = ('item_detail', 'inventory', '123456789|107') 

try:
  # Write a record
  bins={'store':107,
	'upc':123456789,
	'ohqty':16,
	'whrqty':0,
        'transqty':0,
	'writeTime':int(time.time()*1000)
        }
  client.put(key, bins)

except Exception as e:
  import sys
  print("error: {0}".format(e), file=sys.stderr)

# Close the connection to the Aerospike cluster
client.close()
