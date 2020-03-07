from urllib.request import urlopen
import time
import datetime
import os

sleepTime = 45
reconnectTime = 20
path = 'records'

def internet_on():
    isConnected = False
    disconnectTime = datetime.datetime.today()
    reconnectAttempts = 0

    while not isConnected:
        try:
            urlopen('https://www.google.com/', timeout=5)
            #when connection is re-established and the time disconnected is greater than 2 minuets, log the total time of the disconnect
            if(reconnectAttempts > 5): #accounting for lag spikes among other things internet dropage
                with open("records/" + disconnectTime.strftime("%d %b %Y") + ".txt", "a") as f:
                    f.write(disconnectTime.strftime("%H:%M:%S")+" - "+datetime.datetime.today().strftime("%H:%M:%S") + "\n")
                return 'connection is re-established\nlogged time disconnected'
            else:
                return 'connection is stable'
        except:
            print("connection failed")
            reconnectAttempts += 1
            time.sleep(reconnectTime)

if __name__  == "__main__":

    if not os.path.exists(path):
        os.mkdir(path)
        print("Directory "+path+" Created ")
    else:
        print("Directory "+path+" already exists")

    while True:
        print(internet_on())
        time.sleep(sleepTime)