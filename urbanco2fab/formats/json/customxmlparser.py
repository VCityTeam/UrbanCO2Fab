import xml.parsers.expat

#Reference: https://docs.python.org/3.6/library/pyexpat.html

class CustomXMLParser:
  parser = None
  path = []
  value = ""
  identifier_set = False
  identifier = ""
  start_line = -1
  end_line = -1
  data = {}
  features = {}
  def __init__(self, data, features):
    self.parser = xml.parsers.expat.ParserCreate()
    self.parser.StartElementHandler = self.start_element
    self.parser.EndElementHandler = self.end_element
    self.parser.CharacterDataHandler = self.char_data
    self.data = data
    self.features = features
  def start_element(self, name, attrs):
    name = name.strip()
    self.start_line = self.parser.CurrentLineNumber
    for attribute in attrs.keys():
      if (attribute.lower() == "gml:id"):
        self.identifier_set = True
        self.identifier = attrs[attribute]
        self.features[self.identifier] = {}
    if (self.identifier_set):  
      self.data[self.start_line] = {}
      self.data[self.start_line][self.identifier] = {}
      self.path.append(name)
  def end_element(self, name):
    self.end_line = self.parser.CurrentLineNumber
    if (self.identifier_set):
      feature = None
      if self.path:
        feature = self.path.pop()
      key = ".".join(self.path)
      if ("creationdate" not in feature.lower() and
        "terminationdate" not in feature.lower()):
        if (key not in self.data[self.start_line][self.identifier]):
          self.data[self.start_line][self.identifier][key] = {feature: self.value}
        else:
          self.data[self.start_line][self.identifier][key].update({feature, self.value})

      if (key not in self.features[self.identifier]):
        self.features[self.identifier][key] = {feature: self.value}
      else:
        self.features[self.identifier][key].update({feature: self.value})
      if not self.path:
        self.identifier = None
        self.identifier_set = False
        self.path = []
        self.start_line = -1
        self.end_line = -1
    self.value = "" 
  def char_data(self, data):
    data = data.strip()
    if(data != ""):
      if self.value:
        self.value = self.value + " " + data
      else:
        self.value = data
  def parse(self, entryname, text):
    self.parser.Parse(text)
