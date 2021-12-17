from __future__ import print_function,unicode_literals
import subprocess
import time
import sys
import selectors

def connectNetwork():
    global sshProcess 
    sshProcess = subprocess.Popen(['meshctl'],
                               stdin=subprocess.PIPE, 
                               stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE,
                               universal_newlines=True,
                               bufsize=0)
    time.sleep(0.5)
    sshProcess.stdin.write("power off\n")

    sel = selectors.DefaultSelector()
    sel.register(sshProcess.stdout, selectors.EVENT_READ)
    sel.register(sshProcess.stderr, selectors.EVENT_READ)

    while True:
        for key, _ in sel.select():
            data = key.fileobj.read1().decode()
            if not data:
                exit()
            if key.fileobj is sshProcess.stdout:
                print(data, end="")
            else:
                print(data, end="", file=sys.stderr)
    time.sleep(0.5)
    
    sshProcess.stdin.write("power on\n")
    time.sleep(0.5)
    sshProcess.stdin.write("connect 0\n")
    time.sleep(10)

def connectToElement(element):
    sshProcess.stdin.write("menu onoff\n")
    time.sleep(0.5)
    sshProcess.stdin.write("target " + element + " \n")

def toggleLedOn():
    sshProcess.stdin.write("onoff 1\n")
    time.sleep(0.5)

def toggleLedOff():
    sshProcess.stdin.write("onoff 0\n")
    time.sleep(0.5)

connectNetwork()