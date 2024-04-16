import json
import requests
import time
def pincodegeo(a):

    #loginhere: https://geocode.maps.co/
    try:
        print('Pincode extraction')
        url=f'https://geocode.maps.co/search?postalcode={a}&country=IN&api_key=65cc6de0948c4318089132pnw04fd76'
        coordinates_json=requests.get(url)
        return(coordinates_json)
    except:
        return(f'{a} pincode was not found')

