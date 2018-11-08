import requests
import json

send_url = 'http://api.ipstack.com/122.15.164.134?access_key=81bfc1791b638958108b037b7642ad11'
r = requests.get(send_url)
j = json.loads(r.text)
lat = j['latitude']
lon = j['longitude']
add = j['city'] + ", " + j['region_name'] + ", " + j['zip']



send_url = 'https://api.betterdoctor.com/2016-03-01/doctors?location=37.773%2C-122.413%2C100&user_location=37.773%2C-122.413&skip=0&limit=10&user_key=a215b40d8a81855e83b468e64d7c87de'
r = requests.get(send_url)
j = json.loads(r.text)
name =[]
web =[]
latitude =[]
longitude =[]
distance = []
address = []
phone_no=[]
for i in range(10):
    name.append(j['data'][i]['practices'][0]['name'])
    latitude.append(j['data'][i]['practices'][0]['lat'])
    longitude.append(j['data'][i]['practices'][0]['lon'])
    distance.append(j['data'][i]['practices'][0]['distance'])
    address.append(j['data'][i]['practices'][0]["visit_address"]["street"])
    phone_no.append(j['data'][i]['practices'][0]["phones"][0]['number'])