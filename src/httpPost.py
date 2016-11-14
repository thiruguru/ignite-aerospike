import web
import json

        
urls = (
	'/', 'index'
)
app = web.application(urls, globals())

class index:        
	#def POST(self):
	#	data = web.input()
        #	name = data.name
	#	pass1 = data.password

	def POST(self):
        	# How to obtain the name key and then print the value?
	       data = json.loads(web.data())
               name = data["name"]
	       print(name)
	       return "Hello " + name + "!"

if __name__ == "__main__":
    app.run()
