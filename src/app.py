import sys, pprint, re, pymongo
import plotly.graph_objects as go
import plotly.io as pio
from pymongo import MongoClient
import math
import app_consts
import json

# Array that will contain all records in JSON format
FILE = []

# Dictionary to represent the chart
SECURITY_PROTOCOLS = {}

# Records by cities [[tlv], [petha], [haifa], [rishon lezion]]
cities = [[], [], [], []]

# GEO centers
geoCenters = [(app_consts.TLV_lat, app_consts.TLV_lon),(app_consts.PET_TIK_lat, app_consts.PET_TIK_lon),(app_consts.HAIFA_lat, app_consts.HAIFA_lon),(app_consts.RISHON_lat, app_consts.RISHON_lon)]
DEBUG = []
CONST_COMMUNICATION = "WIFI\n"

def securityProtocol_dict_add(arr):
    for p in arr:
        if p in SECURITY_PROTOCOLS:
            SECURITY_PROTOCOLS[p] += 1
        else:
            SECURITY_PROTOCOLS[p] = 1

#/ Reading the file, updating the 'FILE' Array with the Object 'obj',
#  updating the Dictionary 'SECURITY_PROTOCOLS' with the security protocols.
# /#
def readFile(filePath):
    with open(filePath) as fp:
        for cnt, line in enumerate(fp):
            currline = line.split(",")
            # print("line is : {}".format(currline))
            if cnt != 0 and cnt != 1 and currline[-1] == CONST_COMMUNICATION: 
                enc_protocols_line = currline[2][1:-1]
                arr_protocols = enc_protocols_line.split('][')
                securityProtocol_dict_add(arr_protocols)
                obj = {
                    'SSID': currline[1],
                    'MAC': currline[0],
                    'AuthMode': arr_protocols,
                    'Channel': currline[4],
                    'FirstSeen': currline[3],
                    'LAT': currline[6],
                    'LON': currline[7]
                }
                FILE.insert(0, obj)
                DEBUG.insert(0, calcKM_Distance(geoCenters[0], (float(obj['LAT']), float(obj['LON'])), app_consts.EARTH_RADIUS))
                
def readJson(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
        for p in data['results']:
            obj = {
                'SSID': p['ssid'],
                'MAC': p['netid'],
                'AuthMode': p['encryption'],
                'Channel': p['channel'],
                'FirstSeen': p['firsttime'],
                'LAT': p['trilat'],
                'LON': p['trilong']
            }
            FILE.insert(0, obj)
            findcity(obj)


def findcity(obj):
    for i in range(len(geoCenters)):
        dis = calcKM_Distance(geoCenters[i], (float(obj['LAT']), float(obj['LON'])), app_consts.EARTH_RADIUS)
        if dis < 5:
            cities[i].insert(i, obj)


def showDataChart():
    print('[!] Creating Chart ...Loading')
    barX = []
    barY = []
    for key in SECURITY_PROTOCOLS:
        barX.append(key)
        barY.append(SECURITY_PROTOCOLS[key])
    data = [go.Bar(
                x=barX,
                y=barY
        )]

    # py.iplot(data, filename='basic-bar')

    
    data.update_layout(title_text='hello world')
    pio.write_html(data, file='hello_world.html', auto_open=True)


def sendDataToDB():
    if FILE:
        # client = pymongo.MongoClient("mongodb+srv://<USERNAME>:<PASSWORD>@cluster0-qnboi.mongodb.net/test?retryWrites=true&w=majority")
       
        db = client.WIFI
        records = db.records
        # db.records.create_index([('MAC', pymongo.ASCENDING)], unique=True)
        records.insert_many(FILE)
        print("[*] Uploaded, CHECK MongoDB")
    else:
        print("[! ERROR ] Canno't upload the data to MongoDB. ")


def calcKM_Distance(p1, p2, mR):
    lat1, lon1 = p1[0], p1[1]
    lat2, lon2 = p2[0], p2[1]
    points = [lat1, lon1, lat2 , lon2]
    radiants = list(map(math.radians, points))
    lat1, lon1, lat2, lon2 = radiants
    mCOS = math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)
    mSIN = math.sin(lat1) * math.sin(lat2)
    res = math.acos(mSIN + mCOS) * mR
    return res
    
def countEncryption(city):
    protocols_num = {
        'none': 0,
        'wpa' : 0,
        'wpa2' : 0,
        'wep' : 0,
        'unknown': 0
    }
    
    for record in city:
        protocols_num[record['AuthMode']] += 1
    
    return protocols_num

def showCitiesChart(cities):
    citiesNames=['Tel-Aviv', 'Petah-Tikva', 'Haifa', 'Rishon-LeZion']
    fig = go.Figure(data=[
    go.Bar(name='WPA', x=citiesNames, y=[cities[0]['wpa'], cities[1]['wpa'], cities[2]['wpa'], cities[3]['wpa']]),
    go.Bar(name='WPA2', x=citiesNames, y=[cities[0]['wpa2'], cities[1]['wpa2'], cities[2]['wpa2'], cities[3]['wpa2']]),
    go.Bar(name='WEP', x=citiesNames, y=[cities[0]['wep'], cities[1]['wep'], cities[2]['wep'], cities[3]['wep']]),
    go.Bar(name='OPEN', x=citiesNames, y=[cities[0]['none'], cities[1]['none'], cities[2]['none'], cities[3]['none']])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.show()

if __name__ == '__main__' :
    print("[!] Reading File {}  ...Loading".format(sys.argv[1]))
    # readFile(sys.argv[1])

    ## JSON FILE PROCESS
    readJson(sys.argv[1])

    
    TLVEncrypt=countEncryption(cities[0])
    PetahTikvaEncrypt=countEncryption(cities[1])
    HaifaEncrypt=countEncryption(cities[2])
    RishonEncrypt=countEncryption(cities[3])

    showCitiesChart([TLVEncrypt, PetahTikvaEncrypt,HaifaEncrypt,RishonEncrypt])

    if FILE:
        print("[*] Complete Reading With Success!")
    else:
        print("[! ERROR ] ERROR, File Empty Or Bad Format")
    
    # showDataChart()
    # sendDataToDB()
    #  pprint.(FILE)

