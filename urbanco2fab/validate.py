import json
from jsonschema import validate

class Validate:
  """
   Validate a json file. It takes as input a schema file against
   which the json file will be validated.

   Parameters
   ----------
   schemafile: str
     schema file 
   filetovalidate: str
     the JSON file to be validated 

   Returns
   -------
     None

   Raises
   ------ 
     None
  """
  def validatejsonfile(schemafile, filetovalidate):
    with open(filetovalidate, 'r') as jhandle:
      with open(schemafile, 'r') as jshandle:
        jsondata = json.load(jhandle)
        jschema =  json.load(jshandle)
        validate(instance=jsondata, schema=jschema)

