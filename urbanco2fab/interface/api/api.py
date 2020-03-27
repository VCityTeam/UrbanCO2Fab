from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/urbanco2fab/v1.0/workspace', methods=['GET'])
def get_workspace():
    with open("../../../ud-cpov/viz/dist/data.json") as workspacefile:
      workspace = workspacefile.read()
      workspace = json.loads(workspace)
    return jsonify(workspace)

if __name__ == '__main__':
    app.run(debug=True)
