from flask import Flask, jsonify
import json
from formats.json.validate import Validate

app = Flask(__name__)
urbanco2fabport = 8890

"""
returns information required to visualize a workspace
"""
@app.route('/urbanco2fab/v1.0/workspace', methods=['GET'])
def workspace():
    with open("../ud-cpov/viz/dist/data.json") as workspacefile:
      workspace = workspacefile.read()
      workspace = json.loads(workspace)
    return jsonify(workspace)

"""
returns information required to visualize a scenario
"""
@app.route('/urbanco2fab/v1.0/scenario', methods=['GET'])
def scenario():
   pass

"""
returns information required to visualize a version
"""
@app.route('/urbanco2fab/v1.0/versions', methods=['GET'])
def versions():
   jsonstring = "{}"
   return jsonify(jsonstring)

"""
returns information required to visualize a version transition
"""
@app.route('/urbanco2fab/v1.0/versiontransitions', methods=['GET'])
def versiontransitions():
   jsonstring = "{}"
   return jsonify(jsonstring)

"""
returns information required to visualize transactions
"""
@app.route('/urbanco2fab/v1.0/transactions', methods=['GET'])
def transactions():
   jsonstring = "{}"
   return jsonify(jsonstring)


"""
gives a list of all the resources expoosed by urbanco2fab API
"""
@app.route('/urbanco2fab/v1.0/', methods=['GET'])
def operations():
    operations = dict()
    for rule in app.url_map.iter_rules():
      operations[rule.endpoint] = dict()
      operations[rule.endpoint]["resource"] = rule.rule 
      operations[rule.endpoint]["methods"] = list(rule.methods)
    return jsonify(operations)

class API:
   @staticmethod
   def run():
     app.run(debug=True, port=urbanco2fabport)
