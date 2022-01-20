from flask import Flask
import meshctlwrapper as mw

app = Flask(__name__)

@app.route("/")
def test():
    return { 
        "get all node information" : "/get/all",
        "turn node on or off" : "/onoff=<string:target>&<string:onoff>",
        "get node onoff information" : "/get/<string:target>"
    }

@app.route("/get/all")
def getAll():
    return mw.getAllNodes()

@app.route("/get/<string:target>")
def getTargetInformation(target):
    targetState = mw.getget(target)
    return {
        "target" : target,
        "target onoff" : targetState
    }

@app.route("/onoff=<string:target>&<string:onoff>")
def turnNodeOn(target, onoff):
    success = mw.toggleLight(target, onoff)
    return { 
        "target" : target,
        "onoff" : onoff,
        "success" : success
    }

app.run(host='0.0.0.0', port=8090, debug=True)
