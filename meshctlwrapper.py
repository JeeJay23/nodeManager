import os
import subprocess
import json
import time

process = subprocess.Popen(['stdbuf', '-oL', '-i0', 'meshctl'], 
    bufsize=0, 
    stdin=subprocess.PIPE, 
    stdout=subprocess.PIPE
    # universal_newlines=True
)

def init():
    global process
    # start meshctl process
    os.environ['PYTHONUNBUFFERED'] = '1'
    # read opening line
    process.stdout.readline()
    os.set_blocking(process.stdout.fileno(), False)
    connectNetwork()

def connectNetwork():
    global process 
    process.stdin.write("back\n".encode())
    time.sleep(.5)
    process.stdin.write("power off\n".encode())
    time.sleep(0.5)
    process.stdin.write("power on\n".encode())
    time.sleep(0.5)
    process.stdin.write("connect 0\n".encode())
    time.sleep(9)

def getAllNodes():
    msg = ""
    with open("/home/pi/.config/meshctl/prov_db.json", 'r') as file:
        msg = ""
        data = json.load(file)
        for i, p in enumerate(data['nodes']):
            for e in p['configuration']['elements']:
                if "models" in e:
                    msg += str(e) + "\n"
                    # msg += e['unicastAddress'] + "\n"
        return msg

def toggleLight(target, onoff):
    global process
    # just in case
    process.stdin.write("back\n".encode())
    time.sleep(0.5)
    process.stdin.write("menu onoff\n".encode())
    time.sleep(0.5)
    process.stdin.write(("target " + str(target) + "\n").encode())
    time.sleep(0.5)
    process.stdin.write(("onoff " + str(onoff) + "\n").encode())

    while 1:
        try:
            response = process.stdout.readline().decode('utf8')
            if (response == 'Failed to AcquireWrite\n'):
                print("failed to write, restarting network...")
                return -1
        except:
            break
    return 1

def getget(target):
    global process
    process.stdin.write("back\n".encode())
    time.sleep(0.5)
    process.stdin.write("menu onoff\n".encode())
    time.sleep(0.5)
    process.stdin.write(("target " + str(target) + "\n").encode())
    time.sleep(0.5)
    process.stdin.write("get\n".encode())
    time.sleep(0.5)
    while 1:
        try:
            response = process.stdout.readline().decode('utf8')
            if ('On Off Model Message received' in response):
                aresponse = process.stdout.readline().decode('utf8')
                return aresponse[-3]
        except:
            print('didnt get wat we need')
            return -1
            break

    return 1


def getResponse(p):
    while 1:
        try:
            print(p.stdout.readline())
        except:
            break

init()