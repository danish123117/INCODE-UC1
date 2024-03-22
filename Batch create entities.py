import json
import requests

def ngsi_create_entity(d):#updates latest values
    url = 'http://localhost:1026/v2/entities'

    headers = {
    'Content-Type': 'application/json'
    }

    data = d
    response = requests.post(url, json=data, headers=headers)
    return response
   
with open('Operator2.json', 'r') as file:
   op = json.load(file)
    
temp = ngsi_create_entity(op)
print(temp)
with open('Stress2.json', 'r') as file:
   st = json.load(file)
temp2= ngsi_create_entity(st)
print(temp2)

# change this to make it like a loop which seeks all Json files 