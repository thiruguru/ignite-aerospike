import requests
import json

res=requests.get('http://127.0.0.1:8080/?upc=123456789&lat=36.3312292&lang=-94.1491043637163&radius=600')

list1=res.content.split('~')
stores=[]
sellers=[]
address=[]

for x in range(0,list1.__len__()):
	stores=list1[0].split('|')
	sellers=list1[1].split('|')
	address=list1[2].split('|')
print(stores)
print(sellers)
print(address)
