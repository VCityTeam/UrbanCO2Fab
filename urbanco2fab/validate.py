import json

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

  """
   Validate whether an instance belongs to the required class. 
   It takes as input a reference class and the instance to validate 

   Parameters
   ----------
   referenceclass: str
     reference class 
   instancetovalidate: str
     the instance to validate 

   Returns
   -------
     None

   Raises
   ------ 
     Exception
       if they do not match
  """
  def validateclass(referenceclass, instancetovalidate):
    if (instancetovalidate.__class__ != referenceclass):
      raise Exception("The instance " + str(instancetovalidate.__class__) + " is not of the required class :" + str(referenceclass.__class__))
