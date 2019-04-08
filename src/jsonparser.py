import json

def getDifferences(filename):
  with open(filename, 'r') as handle:
      parsed = json.load(handle)
      nodeDict = dict()
      for node in parsed["nodes"]:
        nodeDict[node["id"]] = node["globalid"]
      edgeDict = dict()
      for node in parsed["edges"]:
         if (nodeDict[node["source"]] not in edgeDict):
            edgeDict[nodeDict[node["source"]]] = [] 
         edgeDict[nodeDict[node["source"]]].append(nodeDict[node["target"]])
         print(edgeDict[nodeDict[node["source"]]])

