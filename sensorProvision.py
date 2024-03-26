import requests

# provision service path
url = 'http://localhost:4041/iot/services'
headers = {
    'Content-Type': 'application/json',
    'fiware-service': 'openiot',
    'fiware-servicepath': '/'
}
data = {
    "services": [
        {
            "apikey": "danishabbas",
            "cbroker": "http://orion:1026",
            "entity_type": "Thing",
            "resource": "/iot/json"
        }
    ]
}

response = requests.post(url, json=data, headers=headers)
print(response.status_code)
print(response.text)
#provision EMG sensor
url = 'http://localhost:4041/iot/devices'
headers = {
    'Content-Type': 'application/json',
    'fiware-service': 'openiot',
    'fiware-servicepath': '/'
}
data = {
    "devices": [
        {
            "device_id": "EMG1000",
            "entity_name": "urn:ngsi-ld:Operator:001",
            "entity_type": "Operator",
            "transport":   "MQTT",
            "timezone": "Europe/Berlin",
            "attributes": [
                {"object_id": "TimeStamp", "name": "TimeStamp", "type": "Text"},
                {"object_id": "data", "name": "data", "type": "array"},
                {"object_id": "index", "name": "index", "type": "Integer"},
                {"object_id": "Feaisability", "name": "Feaisability", "type": "array"}
                
            ]

        }
    ]
}

response = requests.post(url, json=data, headers=headers)
print(response.status_code)
print(response.text)