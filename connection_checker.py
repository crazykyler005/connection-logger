import socket
import time
import datetime
import os

sleepTime = 45
reconnectTime = 20
path = 'records' #generated path that stores downtime records

def internet_on():
    isConnected = False
    disconnectTime = datetime.datetime.today()
    reconnectAttempts = 0

    while not isConnected:
        IPaddress = socket.gethostbyname(socket.gethostname())

        if IPaddress != "127.0.0.1":
            #when connection is re-established and the time disconnected is greater than 1 minuet and 40 seconds, log the total time of the disconnect
            if reconnectAttempts >= 5:  #accounting for lag spikes or very brief periods of down time
                with open(path+"/" + disconnectTime.strftime("%d %b %Y") + ".txt", "a") as f:
                    f.write(disconnectTime.strftime("%H:%M:%S")+" - "+datetime.datetime.today().strftime("%H:%M:%S") + "\n")
                return 'connection is re-established\nlogged time disconnected'
            else:
                return 'connection is stable'
        else:
            print("connection attempt failed")

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