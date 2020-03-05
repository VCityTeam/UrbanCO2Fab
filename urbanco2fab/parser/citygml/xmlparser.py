import xml.etree.ElementTree as ET
import dateutil.parser as dateparse
from exception.error import *

def parse(xml):
  root = ET.fromstring(xml)
  versionstartdate = ""
  versionenddate = ""
  for child in root:
    if(child.tag == '{http://www.opengis.net/citygml/1.0}cityObjectMember'):
      cityobjectmember = child.attrib
      for node in child:
        if("{http://www.opengis.net/gml}id" in node.attrib.keys()):
          objectid= node.attrib['{http://www.opengis.net/gml}id']
          for prop in node.findall(".//"):
            if("{http://www.opengis.net/citygml/building/1.0}creationDate" == prop.tag):
              #print("ct:" + prop.text)
              if(versionstartdate == "" or versionstartdate < dateparse.parse(prop.text)):
                versionstartdate = dateparse.parse(prop.text)
            elif("{http://www.opengis.net/citygml/building/1.0}terminationDate" == prop.tag):
              #print("tt: " + prop.text)
              if(versionenddate == "" or versionenddate > dateparse.parse(prop.text)
                 and dateparse.parse(prop.text) > versionstartdate):
                versionenddate = dateparse.parse(prop.text)
  #end for
  #print(versionstartdate, versionenddate)
  if (versionstartdate > versionenddate):
    raise VersionError("Version start date " + str(versionstartdate) + 
                  " after date version end date: " + str(versionenddate))
  return(versionstartdate, versionenddate)
