import requests
import json
url_t = 'http://localhost:1026/v2/subscriptions/'

headers_t = {
    'Content-Type': 'application/json',
    'fiware-service': 'openiot',
    'fiware-servicepath': '/'
}

operator = {
    "description": "Notify QuantumLeap of change in data of emg sensor data and feaisibility attrs",
    "subject": {
        "entities": [
            {
                "idPattern": "Operator.*"
            }
        ],
        "condition": {
            "attrs": [
                "TimeStamp" ,
                "index",
                "data",
                "Feaisability"
                
            ]
        }
    },
    "notification": {
        "http": {
            "url": "http://quantumleap:8668/v2/notify"
        },
        "attrs": [
                "TimeStamp" ,
                "index",
                "data",
                "Feaisability"
        ],
        "metadata": ["dateCreated", "dateModified"]
    }
}

stress = {
    "description": "Notify QuantumLeap of change in data of extracted stress features",
    "subject": {
        "entities": [
            {
                "idPattern": "Stress.*"
            }
        ],
        "condition": {
            "attrs": [
                "medianFrequency" ,
                "meanFrequency",
                "meanPowerFrequency"
                               
            ]
        }
    },
    "notification": {
        "http": {
            "url": "http://quantumleap:8668/v2/notify"
        },
        "attrs": [
                "medianFrequency" ,
                "meanFrequency",
                "meanPowerFrequency"
        ],
        "metadata": ["dateCreated", "dateModified"]
    }
}

response_o = requests.post(url_t, headers=headers_t, data=json.dumps(operator))
response_s = requests.post(url_t, headers=headers_t, data=json.dumps(stress))
