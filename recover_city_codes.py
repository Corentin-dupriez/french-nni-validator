import requests
import json

api_url = 'https://geo.api.gouv.fr/communes/'

def call_geo_api(city_code: str|int): 
    response = requests.get(api_url + str(city_code))
    if response.status_code != 200: 
        return response.status_code, ''
    else:
        response_json = json.loads(response.text)
        return response.status_code, response_json['nom']