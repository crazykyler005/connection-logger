import socket
import time
import datetime
import os
from urllib.request import urlopen

testUrl = 'https://www.google.com/' #reliably active address
path = 'records' #path to stores downtime records
sleepTime = 45
reconnectAttemptTime = 20
disconnectTime = datetime.datetime.today()

def router_connected():

    routerConnectAttempts = 0

    while True:

        IPaddress = socket.gethostbyname(socket.gethostname())

        if IPaddress != "127.0.0.1":
            #when connection is re-established after x amount of reconnect attemps, log the total time of the disconnect
            if routerConnectAttempts >= 3: #don't log if connection is down briefly
                log_disconnect("router")
                return False
            else:
                print('connected with router')
            return True
        else:
            routerConnectAttempts += 1
            print("Failed to establish connection with router")
            time.sleep(reconnectAttemptTime)

def internet_on():

    internetConnectAttempts = 0

    while True:

        try:
            urlopen("https://www.google.com/", timeout=5)
            ##when connection is re-established after x amount of reconnect attemps, log the total time of the disconnect
            if(internetConnectAttempts >= 5): #accounting for lag spikes among other things internet dropage issues
                log_disconnect("internet")
            else:
                print('connection to internet is stable')

            internetConnectAttempts = 0
            time.sleep(sleepTime)

        except:
            print('Failed to connect to url')

            if internetConnectAttempts == 0:
                disconnectTime = datetime.datetime.today()#ensure that the intial disconnect time is accurate

            if(router_connected() != True):#returns false if the connection issue is with the router. 
                internetConnectAttempts = 0
            else:
                internetConnectAttempts += 1
            time.sleep(reconnectAttemptTime)

def log_disconnect(connection): #print total time interval of disconnect to text file

    try:
        with open("records/" + disconnectTime.strftime("%d %b %Y") + ".txt", "a") as f:
            f.write("Time disconnected from "+connection+": "+disconnectTime.strftime("%d %b %H:%M:%S")+" - "+datetime.datetime.today().strftime("%d %b %H:%M:%S") + "\n")
        print('Connection is re-established\nlogged time disconnected from '+connection)
    except:
        print('Issue with logging record')

if __name__  == "__main__":

    if not os.path.exists(path):
        os.mkdir(path)
        print("Directory path "+"../"+path+" created")
    else:
        print("Directory path "+"../"+path+" already exists")

    internet_on()