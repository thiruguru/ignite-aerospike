from __future__ import print_function
import web
import aerospike
from aerospike import GeoJSON
from aerospike import predicates as p
import json
import pprint

# Configure the client
config = {
  'hosts': [ ('127.0.0.1', 3000) ]
}

# Create a client and connect it to the cluster
        
urls = (
    '/(.*)', 'invprice'
)
app = web.application(urls, globals())

class invprice:        
     def GET(self, name):
	request_params = web.input()	
  	print(request_params.lat)
	print(request_params.lang)
	latitude=float(request_params.lat)
	langitude=float(request_params.lang)
	radius=int(request_params.radius)
	#pp = pprint.PrettyPrinter(indent=2)
	try:
	    client = aerospike.client(config).connect()
	   # Records are addressable via a tuple of (namespace, set, key)
	    query = client.query('locality', 'location')
	    query.select('store','seller','address','loc')
	    query.where(p.geo_within_radius('loc', langitude, latitude, radius))

	    stores = []
 	    sellers = []
            address = []

	    def matched_names((key, metadata, bins)):
		    #pp.pprint(bins)
		    stores.append(bins['store'])
		    sellers.append(bins['seller'])
		    address.append(bins['address'])
		    
	    query.foreach(matched_names)
	    
	    storeStr=''
	    addressStr=''
	    sellerStr=''
	    for i in range(0,stores .__len__()):
		 storeStr=storeStr+str(stores[i])+'|'
		 addressStr=addressStr+address[i]+'|'
		 sellerStr=sellerStr+sellers[i]+'|'
	    response=storeStr[:-1]+'~'+sellerStr[:-1]+'~'+addressStr[:-1]
	   
	    print("Final response::",response)

	    return response

	    # Close the connection to the Aerospike cluster
	    client.close()

	except Exception as e:
            import sys
            print("error: {0}".format(e), file=sys.stderr)
if __name__ == "__main__":
    app.run()
