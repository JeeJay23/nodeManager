from flask import Flask
import meshctlwrapper as mw

app = Flask(__name__)
meshCtl = mw.meshCtlWrapper()

@app.route("/")
def test():
    return { 
        "get all node information" : "/get/all",
        "turn node on or off" : "/onoff=<string:target>&<string:onoff>",
        "get node onoff information" : "/get/<string:target>"
    }

@app.route("/provision/scan")
def provisionScan():
    return {
        "Not implemented yet" : 0,
        "Will return list of unprovisioned nodes" : 0
    }

@app.route("/provision/<string:target>")
def provisionTarget(target):
    return {
        "Not implemented yet" : 0
    }

@app.route("/get/all")
def getAll():
    return meshCtl.getAllNodes()

@app.route("/get/<string:target>")
def getTargetInformation(target):
    global targetState 
    targetState = meshCtl.getget(target)
    while (targetState == -1):
        targetState = meshCtl.getget(target)
    return {
        "target" : target,
        "target onoff" : targetState
    }

@app.route("/onoff=<string:target>&<string:onoff>")
def turnNodeOn(target, onoff):
    success = meshCtl.toggleLight(target, onoff)
    return { 
        "target" : target,
        "onoff" : onoff,
        "success" : success
    }

app.run(host='0.0.0.0', port=8090, debug=True)
