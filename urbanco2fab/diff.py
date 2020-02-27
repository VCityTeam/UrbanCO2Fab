from pygit2 import Repository
from parser.citygml.customxmlparser import CustomXMLParser
import xml.etree.ElementTree as ET
import json
from xml.etree.ElementTree import XMLParser
from dateutil.parser import parse

def verify_dates(time1, time2):
  if(parse(time1) > parse(time2)):
     raise ValueError('Check existence times of version')

def get_transactions(repository, version1, version2, start_time="",
       end_time="", use_citygml=False, display=False, detailed=False):
  transactions = []
  repo = Repository(repository)
  diff = repo.diff(version1, version2, context_lines=0)
  if(display):
    with open(".urbanco2fab/versions.json", "r") as jsonfile:
      versionsmetadata = json.load(jsonfile)
      if version1 in versionsmetadata and version2 in versionsmetadata:
        start_time = versionsmetadata[version1]["existenceendtime"]
        end_time = versionsmetadata[version2]["existencestarttime"]
      else:
        print("Warning: No physical existence time available")
       
  datav1 = dict()
  datav2 = dict()
  featuresv1 = dict()
  featuresv2 = dict()
  commit = repo.get(version1) 
  if (commit is not None):
   tree = commit.tree
   for entry in tree:
     print("entry")
     if(".xml" in entry.name or ".gml" in entry.name):
        blob = repo[entry.id]
        parser = CustomXMLParser(datav1, featuresv1)
        parser.parse(entry.name, blob.read_raw().decode('utf-8'))

  commit = repo.get(version2) 
  if (commit is not None):
   tree = commit.tree
   for entry in tree:
     if(".xml" in entry.name or ".gml" in entry.name):
        blob = repo[entry.id]
        parser = CustomXMLParser(datav2, featuresv2)
        parser.parse(entry.name, blob.read_raw().decode('utf-8'))

  print(datav1)
  print(datav2)
  for patch in diff:
    for hunk in patch.hunks:
      print(hunk)
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
        print("change" + str(change))
        transaction = {}
        if change in datav2:
          gmlid = next(iter(datav2[change].keys()))
          print("gmlid" + gmlid)
          for feature in datav2[change][gmlid]:
            attribute = next(iter(datav2[change][gmlid][feature].keys()))
            transaction["id"] = gmlid+"#"+attribute
            if(detailed == True):
              transaction["featureid"] = gmlid+"#"+attribute
              transaction[attribute] = featuresv2[gmlid][feature][attribute]
            transaction["type"] = "Replace"
            transaction_existencestarttime = None
            transaction_existenceendtime = None
            for attribute in featuresv2[gmlid][feature]: 
              if(use_citygml):
                if("creationdate" in attribute.lower()):
                  transaction_existencestarttime = featuresv2[gmlid][feature][attribute]
                elif("terminationdate" in attribute.lower()):
                  transaction_existenceendtime = featuresv2[gmlid][feature][attribute]
              else:
                transaction_existencestarttime = start_time 
                transaction_existenceendtime = end_time 
            if(display!= True):
              verify_dates(transaction_existencestarttime,
                transaction_existenceendtime)
            if(detailed == True):
               transaction["existencestarttime"] = transaction_existencestarttime
               transaction["existenceendtime"] = transaction_existenceendtime
        if transaction:
          transactions.append(transaction)
      for change in inserts:
        print("insert" + str(change))
        transaction = {}
        if change in datav2:
          gmlid = next(iter(datav2[change].keys()))
          print("gmlid" + gmlid)
          for feature in datav2[change][gmlid]:
            print("feature")
            attribute = next(iter(datav2[change][gmlid][feature].keys()))
            transaction["id"] = gmlid+"#"+attribute
            if(detailed == True):
              transaction["featureid"] = gmlid+"#"+attribute
              transaction[attribute] = featuresv2[gmlid][feature][attribute]
            transaction["type"] = "Insert"
            for attribute in featuresv2[gmlid][feature]: 
              if(use_citygml):
                if("creationdate" in attribute.lower()):
                  transaction_existencestarttime = featuresv2[gmlid][feature][attribute]
                elif("terminationdate" in attribute.lower()):
                  transaction_existenceendtime = featuresv2[gmlid][feature][attribute]
              else:
                transaction_existencestarttime = start_time 
                transaction_existenceendtime = end_time 
            verify_dates(transaction_existencestarttime,
               transaction_existenceendtime)
            if(detailed == True):
               transaction["existencestarttime"] = transaction_existencestarttime
               transaction["existenceendtime"] = transaction_existenceendtime
        if transaction:
          transactions.append(transaction)
      for change in deletes:
        print("delete" + str(change))
        transaction = {}
        if change in datav1:
          gmlid = next(iter(datav1[change].keys()))
          print("gmlid" + gmlid)
          for feature in datav1[change][gmlid]:
            attribute = next(iter(datav1[change][gmlid][feature].keys()))
            transaction["id"] = gmlid+"#"+attribute
            if(detailed == True):
              transaction["featureid"] = gmlid+"#"+attribute
              transaction[attribute] = featuresv1[gmlid][feature][attribute]
            transaction["type"] = "Delete"
            for attribute in featuresv1[gmlid][feature]: 
              if(use_citygml):
                if("creationdate" in attribute.lower()):
                  transaction_existencestarttime = featuresv1[gmlid][feature][attribute]
                elif("terminationdate" in attribute.lower()):
                  transaction_existenceendtime = featuresv1[gmlid][feature][attribute]
              else:
                transaction_existencestarttime = start_time 
                transaction_existenceendtime = end_time 
            verify_dates(transaction_existencestarttime,
               transaction_existenceendtime)
            if(detailed == True):
               transaction["existencestarttime"] = transaction_existencestarttime
               transaction["existenceendtime"] = transaction_existenceendtime
        if transaction:
          transactions.append(transaction)
  if(display):
     print(transactions)
  return transactions
