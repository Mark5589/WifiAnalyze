import sys, pprint, re, pymongo
import plotly.plotly as py
import plotly.graph_objs as go
from pymongo import MongoClient

# Array that will contain all records in JSON format
FILE = []

# Dictionary to represent the chart
SECURITY_PROTOCOLS = {}


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
                }
                FILE.insert(0, obj)
                
                # print("{} ) line is : {}, LAST ELEMENT:: {}".format(cnt,currline, currline[-1]))
                # print("obj:: {}".format(obj))

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

    py.iplot(data, filename='basic-bar')


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

if __name__ == '__main__' :
    print("[!] Reading File {}  ...Loading".format(sys.argv[1]))
    readFile(sys.argv[1])
    
    #DEBUG#
    pprint.pprint(FILE)
    
    if FILE:
        print("[*] Complete Reading With Success!")
    else:
        print("[! ERROR ] ERROR, File Empty Or Bad Format")
    
    showDataChart()
    sendDataToDB()
    # print(FILE)

