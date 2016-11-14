# import the module
from __future__ import print_function
import aerospike

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
key = ('ignite', 'inventory', 'upcstore')

try:
  # Write a record
  client.put(key, {'ohqty': 10})

except Exception as e:
  import sys
  print("error: {0}".format(e), file=sys.stderr)

# Close the connection to the Aerospike cluster
client.close()
