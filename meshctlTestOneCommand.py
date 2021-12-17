import subprocess

#test code 
command = 'meshctl'
args = 'mesh-info'
stringToSearchFor = 'deviceKey'
offset = 3


# open subprocess with command and arguments and return output
def execCommand(command, args):
    process = subprocess.Popen([command, args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    process.wait() 
    return stdout

# check stdout for a string
def checkReturn(stringToSearchFor, stdout, offset):
    if(stdout.find(stringToSearchFor) != -1): 
        pos = stdout.find(stringToSearchFor)
        string = stdout[pos:pos + len(stringToSearchFor) + offset + 32]
        return string
    else:
        return stringToSearchFor + 'not found'

output = execCommand(command, args)
print(checkReturn(stringToSearchFor, output, 3))