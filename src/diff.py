from pygit2 import Repository
from customxmlparser import CustomXMLParser
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLParser

def get_transactions(repository, version1, version2):
  transactions = []
  repo = Repository(repository)
  diff = repo.diff(version1, version2, context_lines=0)
  datav1 = dict()
  datav2 = dict()
  featuresv1 = dict()
  featuresv2 = dict()
  commit = repo.get(version1) 
  if (commit is not None):
   tree = commit.tree
   for entry in tree:
     if(".xml" in entry.name):
        blob = repo[entry.id]
        parser = CustomXMLParser(datav1, featuresv1)
        parser.parse(entry.name, blob.read_raw().decode('utf-8'))

  commit = repo.get(version2) 
  if (commit is not None):
   tree = commit.tree
   for entry in tree:
     if(".xml" in entry.name):
        blob = repo[entry.id]
        parser = CustomXMLParser(datav2, featuresv2)
        parser.parse(entry.name, blob.read_raw().decode('utf-8'))

  for patch in diff:
    for hunk in patch.hunks:
      changes = []
      deletes = []
      inserts = []
      for line in hunk.lines:
        if(line.origin == "+"):
          if(line.new_lineno in deletes): #modify
            changes.append(line.new_lineno) 
            deletes.remove(line.new_lineno)
          else: #insert
            inserts.append(line.new_lineno) 
        elif(line.origin == "-"): 
            deletes.append(line.old_lineno)
      for change in changes:
        if change in datav2:
          gmlid = next(iter(datav2[change].keys()))
          transaction = {}
          for feature in datav2[change][gmlid]:
            attribute = next(iter(datav2[change][gmlid][feature].keys()))
            transaction["id"] = gmlid+"#"+attribute
            transaction["featureid"] = gmlid+"#"+attribute
            transaction["type"] = "Replace"
            transaction[attribute] = featuresv2[gmlid][feature][attribute]
            for attribute in featuresv2[gmlid][feature]: 
              if("creationdate" in attribute.lower()):
                transaction["creationdate"] = featuresv2[gmlid][feature][attribute]
              elif("terminationdate" in attribute.lower()):
                transaction["terminationdate"] = featuresv2[gmlid][feature][attribute]
        if transaction:
          transactions.append(transaction)
      for change in inserts:
        if change in datav2:
          gmlid = next(iter(datav2[change].keys()))
          transaction = {}
          for feature in datav2[change][gmlid]:
            attribute = next(iter(datav2[change][gmlid][feature].keys()))
            transaction["id"] = gmlid+"#"+attribute
            transaction["featureid"] = gmlid+"#"+attribute
            transaction["type"] = "Insert"
            transaction[attribute] = featuresv2[gmlid][feature][attribute]
            for attribute in featuresv2[gmlid][feature]: 
              if("creationdate" in attribute.lower()):
                transaction["creationdate"] = featuresv2[gmlid][feature][attribute]
              elif("terminationdate" in attribute.lower()):
                transaction["terminationdate"] = featuresv2[gmlid][feature][attribute]
        if transaction:
          transactions.append(transaction)
      for change in deletes:
        if change in datav1:
          gmlid = next(iter(datav1[change].keys()))
          transaction = {}
          for feature in datav1[change][gmlid]:
            attribute = next(iter(datav1[change][gmlid][feature].keys()))
            transaction["id"] = gmlid+"#"+attribute
            transaction["featureid"] = gmlid+"#"+attribute
            transaction["type"] = "Delete"
            transaction[attribute] = featuresv1[gmlid][feature][attribute]
            for attribute in featuresv1[gmlid][feature]: 
              if("creationdate" in attribute.lower()):
                transaction["creationdate"] = featuresv1[gmlid][feature][attribute]
              elif("terminationdate" in attribute.lower()):
                transaction["terminationdate"] = featuresv1[gmlid][feature][attribute]
        if transaction:
          transactions.append(transaction)
  return transactions
