import json
from jsonschema import validate

def validatefiles(versionsfile, workspacefile, scenariosfile):
  with open(versionsfile, 'r') as jhandle:
    with open('schema/versions.schema.json', 'r') as jshandle:
      print("Validating versions")
      jsondata = json.load(jhandle)
      jschema =  json.load(jshandle)
      validate(instance=jsondata, schema=jschema)
      print("  Ok")
  
  with open(workspacefile, 'r') as jhandle:
    with open('schema/workspace.schema.json', 'r') as jshandle:
      print("Validating workspace")
      jsondata = json.load(jhandle)
      jschema =  json.load(jshandle)
      validate(instance=jsondata, schema=jschema)
      print("  Ok")
  
  with open(scenariosfile, 'r') as jhandle:
    with open('schema/scenarios.schema.json', 'r') as jshandle:
      print("Validating scenarios")
      jsondata = json.load(jhandle)
      jschema =  json.load(jshandle)
      validate(instance=jsondata, schema=jschema)
      print("  Ok")


validatefiles('versions.json', 'workspace.json', 'scenarios.json')
