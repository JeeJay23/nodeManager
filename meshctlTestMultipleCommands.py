import subprocess

#test code 
command = "meshctl"
args = 'mesh-info'
stringToSearchFor = 'deviceKey'
offset = 3

process = subprocess.Popen(['meshctl'], text=True, shell=True)
stdout, stderr = process.communicate('HELLO?')
process.wait() 