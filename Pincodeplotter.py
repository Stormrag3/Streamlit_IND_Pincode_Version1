import streamlit as st
from openrouteservice import convert
import folium
import geocoder_harsh
import requests
import time
from streamlit_folium import folium_static
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from io import StringIO

def distance(lat1, lat2, lon1, lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return (c * r)

def mapmaker(output_pincodes):

    coords=[]
    bodycord=[]
    totalpc= len(output_pincodes)
    for i in output_pincodes:
        lon=i['lon']
        lat=i['lat']
        name=i['name']
        pincode=i['postalcode']
        incord= float(lat),float(lon)
        coords.append(incord)
        inbody=[float(lon),float(lat)]
        bodycord.append(inbody)

    #coords = str(tcoords).replace('[','(').replace(']',')').replace("'","")
    print('coords')
    print(coords)
    #newbodycord = list(str(bodycord).replace("'",""))
    #coords = ((8.681495, 49.41461), (8.686507, 49.41943), (8.687872, 49.420318))

    body = {"coordinates": bodycord,
            "radiuses": [-1]}
    print(body)
    # body = {"coordinates":[[8.681495,49.41461],[8.686507,49.41943],[8.687872,49.420318]],
    #         "radiuses":[-1]}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': '5b3ce3597851110001cf62488731ce752b0a4577b1907df93600c424',
        'Content-Type': 'application/json; charset=utf-8'
    }

    res = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/json', json=body, headers=headers)
    print(res.json())
    time.sleep(2)
    geometry = res.json()['routes'][0]['geometry']
    decoded = convert.decode_polyline(geometry)

    #distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res.json()['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
    #duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res.json()['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"

    m = folium.Map(location=[20.5937,78.9629],zoom_start=5, control_scale=True,tiles="cartodbpositron")
    folium.GeoJson(decoded).add_child(folium.Popup(max_width=30000)).add_to(m)

    folium.Marker(
        location=coords[0],
        popup="Galle fort",
        icon=folium.Icon(color="black"),
    ).add_to(m)

    folium.Marker(
        location=coords[1],
        popup="Jungle beach",
        icon=folium.Icon(color="black"),
    ).add_to(m)

    folium.Marker(
        location=coords[2],
        popup="Jungle beach",
        icon=folium.Icon(color="black"),
    ).add_to(m)

    folium.Marker(
        location=coords[3],
        popup="Jungle beach",
        icon=folium.Icon(color="black"),
    ).add_to(m)
    #
    # folium.Marker(
    #     location=coords[4],
    #     popup="Jungle beach",
    #     icon=folium.Icon(color="black"),
    # ).add_to(m)
    #
    # folium.Marker(
    #     location=coords[5],
    #     popup="Jungle beach",
    #     icon=folium.Icon(color="black"),
    # ).add_to(m)
    #location=list(coords[4][::-1]),
    folium_static(m)
    #m.save('map.html')



#pc1='400097'
#pc2='400083'
# pc3='401107'
# pc4='440001'
# pc5='401101'


col1,col2 = st.columns(2)
pc1 = col1.text_input("Pincode 1 ex: 400097")
#col1.write(geocoder_harsh.pincodegeo(pc1))
pc2 = col1.text_input("Pincode 2 ex: 401107")
#col1.write(geocoder_harsh.pincodegeo(pc2))
pc3 = col2.text_input("Pincode 3 ex: 400080")
#col1.write(geocoder_harsh.pincodegeo(pc3))
pc4 = col2.text_input("Pincode 4 ex: 400067")
#col1.write(geocoder_harsh.pincodegeo(pc4))

input_pincodes=[pc1,pc2,pc3,pc4]
totalpc = len(input_pincodes)
output_pincodes=[]
pincode_counter=4


for a in input_pincodes:
    print('-----')
    print(a)
    coordinates_json =(geocoder_harsh.pincodegeo(a))
    time.sleep(2)
    pincode_extracted={
        'postalcode':str(a),
        'lat':coordinates_json.json()[0]['lat'],
        'lon':coordinates_json.json()[0]['lon'],
        'name':coordinates_json.json()[0]['display_name']
    }
    # try:
    #     col2.success(f'Success! lat:{round(float(pincode_extracted["lat"]),3)}, lon:{round(float(pincode_extracted["lon"]),3)}')
    # except:
    #     col2.error('No response from Geocode API')
    output_pincodes.append(pincode_extracted)

print(output_pincodes)

#For Orthodromic calculations
name1=output_pincodes[0]['name']
lat1=float(output_pincodes[0]['lat'])
lon1=float(output_pincodes[0]['lon'])

name2=output_pincodes[1]['name']
lat2=float(output_pincodes[1]['lat'])
lon2=float(output_pincodes[1]['lon'])

#orthodromic distance
print('Orthodromic distance:')
print(f'location 1: pincode:{pc1}, name:{name1}')
print(f'location 2: pincode:{pc2}, name:{name2}')
print(distance(lat1, lat2, lon1, lon2), "K.M")

testresult=f'Orthodromic distance between {pc1} & {pc2} is {distance(lat1, lat2, lon1, lon2)} KMS'
df = pd.DataFrame()
StringData = StringIO(testresult)

df1 = pd.read_csv(StringData, sep =";")
@st.cache_data
def convert_df(df1):
   return df1.to_csv(index=False).encode('utf-8')
csv = convert_df(df)

st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)
testresult
mapmaker(output_pincodes)
