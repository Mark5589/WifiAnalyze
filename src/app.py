import sys, pprint, re
import plotly.plotly as py
import plotly.graph_objs as go

FILE = []
SECURITY_PROTOCOLS = []

CONST_COMMUNICATION = "WIFI\n"

def readFile(filePath):
    with open(filePath) as fp:
        for cnt, line in enumerate(fp):
            currline = line.split(",")
            # print("line is : {}".format(currline))
            if cnt != 0 and cnt != 1 and currline[-1] == CONST_COMMUNICATION: 
                enc_protocols_line = currline[2][1:-1]
                arr_protocols = enc_protocols_line.split('][')

                obj = {
                    'SSID': currline[1],
                    'MAC': currline[0],
                    'AuthMode': arr_protocols,
                    'Channel': currline[4],
                    'FirstSeen': currline[3],
                }
                FILE.append(obj)
                # print("{} ) line is : {}, LAST ELEMENT:: {}".format(cnt,currline, currline[-1]))
                # print("obj:: {}".format(obj))

def showDataChart():
    print('[!] Creating Chart ...Loading')

    data = [go.Bar(
                x=['giraffes', 'orangutans', 'monkeys'],
                y=[20, 14, 23]
        )]

    py.iplot(data, filename='basic-bar')


if __name__ == '__main__' :
    print("[!] Reading File {}  ...Loading".format(sys.argv[1]))
    readFile(sys.argv[1])
    
    #DEBUG#
    # pprint.pprint(FILE)
    
    if FILE:
        print("[*] Complete Reading With Success!")
    else:
        print("[! ERROR ] ERROR, File Empty Or Bad Format")
    

    showDataChart()
    # print(FILE)
    
    
