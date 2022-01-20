from flask import Flask
import meshctlwrapper

app = Flask(__name__)

@app.route("/")
def test():
    return { "does this" : "work?" }

@app.route("/getnames")
def myFun():
    return { "name" : __name__, 'test' : 'test2' }

@app.route("/get/all")
def getget():
    return meshctlwrapper.getAllNodes()

app.run(host='0.0.0.0', port=8090, debug=True)
