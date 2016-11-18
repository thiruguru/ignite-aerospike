from __future__ import print_function
import web
import aerospike
from aerospike import GeoJSON
from aerospike import predicates as p
import json

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
	try:
	    client = aerospike.client(config).connect()
	   # Records are addressable via a tuple of (namespace, set, key)
	    query = client.query('locality', 'location')
	    query.select('store','seller','address','loc')
	    query.where(p.geo_within_radius('loc', -94.2217082259192, 36.3689382317293, 1000))
	    stores = []
 	    sellers = []
            address = []
	    ohqty = []
	    price = []
	    upc='123456789'+'|'	    
	    def matched_names((key, metadata, bins)):
		    stores.append(bins['store'])
		    sellers.append(bins['seller'])
		    address.append(bins['address'])
		    
	    query.foreach(matched_names)
	
	    def fetch_inv_price():
		for i in range(0,stores .__len__()):
		    key=upc+str(stores[i])
		    keyInv = ('item_detail', 'inventory', key)
                    #Read a record
                    (key, metadata, record) = client.get(keyInv)
                    ohqty.append(record.get('ohqty'))

                    keyPrice = ('item_detail', 'price', '55667788|100')
                    (key, metadata, record) = client.get(keyPrice)
                    price.append(record.get('sellprice'))

	    fetch_inv_price()

	    #pp.pprint(stores[1])
	    #pp.pprint(sellers)
	    startTag = '{"product": { "upc": 1234567,"details": ['
	    endTag='] } }'
	    response=startTag 
	    for x in range(0, sellers.__len__()):
		res='{"seller":'+ sellers[x] +'],"address": '+address[x]+',"inventory": {"available": '+str(ohqty[x])+'},"price": '+str(price[x])+'}'
		response=response+res+','
	    # Close the connection to the Aerospike cluster
	    client.close()
	    return json.dumps(response[:-1]+endTag,indent=4)
	    #return response[:-1]+endTag

	except Exception as e:
            import sys
            print("error: {0}".format(e), file=sys.stderr)
if __name__ == "__main__":
    app.run()
