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
	request_params = web.input()	
  	print(request_params.lat)
	print(request_params.lang)
	#latitude=36.3312292
	#langitude=-94.1491043637163
	upc=str(request_params.upc)
	latitude=float(request_params.lat)
	langitude=float(request_params.lang)
	radius=int(request_params.radius)
	try:
	    client = aerospike.client(config).connect()

	   # Records are addressable via a tuple of (namespace, set, key)
	    query = client.query('locality', 'location')
	    query.select('store','seller','address','loc')
	    query.where(p.geo_within_radius('loc', langitude, latitude, radius))

	    stores = []
 	    sellers = []
            address = []
	    ohqty = []
	    price = []
	    upc1=upc+'|'	    

	    #response=requests.get('http://127.0.0.1:8080/?upc=123456789&lat=36.3369605&lang=-94.2215415&radius=600')
	    #list1=res.content.split('~')

	    #for x in range(0,list1.__len__()):
        	#stores=list1[0].split('|')
	        #sellers=list1[1].split('|')
        	#address=list1[2].split('|')
	    
	    def matched_names((key, metadata, bins)):
		    stores.append(bins['store'])
		    sellers.append(bins['seller'])
		    address.append(bins['address'])
		    
	    query.foreach(matched_names)
	
	    def fetch_inv_price():
		for i in range(0,stores .__len__()):
		    key=upc1+str(stores[i])
		    print("KEY::",key)
		    
		    keyInv = ('item_detail', 'inventory', key)
                    #Read a record
                    (key, metadata, record) = client.get(keyInv)
                    ohqty.append(record.get('ohqty'))
		    
		    key2=upc1+str(stores[i])
                    keyPrice = ('item_detail', 'price', key2)
                    (key, metadata, record) = client.get(keyPrice)
                    price.append(record.get('sellprice'))

	    fetch_inv_price()

	    #pp.pprint(stores[1])
	    #pp.pprint(sellers)
	    startTag = '{"product": { "upc": '+upc+',"details": ['
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
