import os
import subprocess
import json
import time

class meshCtlWrapper:
    process = None

    def __init__(self):
        self.process = subprocess.Popen(['stdbuf', '-oL', '-i0', 'meshctl'], 
            bufsize=0, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE
            # universal_newlines=True
        )
        os.environ['PYTHONUNBUFFERED'] = '1'
        # read opening line
        self.process.stdout.readline()
        os.set_blocking(self.process.stdout.fileno(), False)
        self.connectNetwork()


    def connectNetwork(self):
        self.process.stdin.write("back\n".encode())
        time.sleep(0.5)
        self.process.stdin.write("power off\n".encode())
        time.sleep(0.5)
        self.process.stdin.write("power on\n".encode())
        time.sleep(0.5)
        self.process.stdin.write("connect 0\n".encode())
        time.sleep(9)

    def close(self):
        self.self.process.stdin.write("quit\n".encode())
        time.sleep(.5)
        self.self.process.terminate()

    def getAllNodes(self):
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

    def toggleLight(self, target, onoff):
        # just in case
        self.process.stdin.write("back\n".encode())
        time.sleep(0.5)
        self.process.stdin.write("menu onoff\n".encode())
        time.sleep(0.5)
        self.process.stdin.write(("target " + str(target) + "\n").encode())
        time.sleep(0.5)
        self.process.stdin.write(("onoff " + str(onoff) + "\n").encode())

        while 1:
            try:
                response = self.process.stdout.readline().decode('utf8')
                if (response == 'Failed to AcquireWrite\n'):
                    print("failed to write, restarting network...")
                    return -1
            except:
                break

        return 1

    def getget(self, target):
        self.process.stdin.write("back\n".encode())
        time.sleep(0.5)
        self.process.stdin.write("menu onoff\n".encode())
        time.sleep(0.5)
        self.process.stdin.write(("target " + str(target) + "\n").encode())
        time.sleep(0.5)
        self.process.stdin.write("get\n".encode())
        time.sleep(0.5)
        while 1:
            try:
                response = self.process.stdout.readline().decode('utf8')
                if ('On Off Model Message received' in response):
                    aresponse = self.process.stdout.readline().decode('utf8')
                    return aresponse[-3]
            except:
                print('didnt get wat we need')
                break

        return 1


    def getResponse(self, p):
        while 1:
            try:
                print(p.stdout.readline())
            except:
                break

    def discoverUnprovisioned(self):
        self.process.stdin.write("back\n".encode())
        time.sleep(0.5)
        self.process.stdin.write("discover-unprovisioned on\n".encode())
        print("Discovering...")
        time.sleep(5)
        UUIDs = []
        while (self.process.stdout.readable() != type(None)):
            try:
                response = self.process.stdout.readline().decode('utf8')
                if ('Device UUID: ' in response):
                    index = response.find("Device UUID: ")
                    UUIDs.append(response[index+13:])
            except:
                if not UUIDs:
                    print('No unprovioned devices found.')
                break
        return UUIDs

    # returns button presses
    def provisionNode(self, UUID):
        self.process.stdin.write(("provision " + str(UUID) + "\n").encode())
        print("Provisioning device... Please wait until lights flicker.")
        time.sleep(15)
        while (self.process.stdout.readable() != type(None)):
            try:
                response = self.process.stdout.readline().decode('utf8')
                if ('Agent String: Push' in response):
                    index = response.find("Push")
                    # print amount of times to push button
                    print("Push button " + response[index+5:index+6] + "x times to provision.")
                    return response[index+5:index+6]
                if ('Failed to start provisioning' in response):
                    print('Provisioning failed. Discover and try again.')
                    self.process.stdin.write("some garbage to get out of fake provisioning state".encode())
                    return -2
            except:
                return -1

    # returns unicast number
    def checkProvisionSucces(self):
        while 1:
            try:
                response = self.process.stdout.readline().decode('utf8')
                if ('Provision success. Assigned Primary Unicast' in response):
                    index = response.find("Unicast")
                    # unicast number is 4 characters long
                    print("Provision success. Assigned Primary Unicast " + response[index+8:index+12])
                    return response[index+8:index+12]
            except:
                print('Provisioning failed. Please try again.')
                return -1
    
    # add appkey
    def addAppKey(self, unicastNumber):
        self.process.stdin.write("back\n".encode())
        time.sleep(0.5)
        self.process.stdin.write("menu config\n".encode())
        time.sleep(0.5)
        self.process.stdin.write(("target " + str(unicastNumber) + "\n").encode())
        time.sleep(0.5)
        self.process.stdin.write(("appkey-add 1\n").encode())
        time.sleep(0.5)
        self.process.stdin.write(("bind 0 1 1000\n").encode())
        time.sleep(0.5)
        while 1:
            try:
                response = self.process.stdout.readline().decode('utf8')
                if ('Model App status Success' in response):
                    print("AppKey and bind succes")
                    return 1
                if ('Failed to AcquireWrite' in response):
                    print("Failed to AcquireWrite, restarting network... try again after")
                    self.connectNetwork()
                    return -2
            except:
                print('Garbage')
                return -1