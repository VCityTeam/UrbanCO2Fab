from flask import Flask, jsonify
import json

app = Flask(__name__)
urbanco2fabport = 8890

"""
returns information required to visualize a workspace
"""
@app.route('/urbanco2fab/v1.0/workspace', methods=['GET'])
def workspace():
    with open("../../../ud-cpov/viz/dist/data.json") as workspacefile:
      workspace = workspacefile.read()
      workspace = json.loads(workspace)
    return jsonify(workspace)

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
      #print(dir(rule))
    return jsonify(operations)

if __name__ == '__main__':
    app.run(debug=True, port=urbanco2fabport)
