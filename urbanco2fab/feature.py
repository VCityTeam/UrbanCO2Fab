from abstractfeature import AbstractFeature
from dateutil.parser import parse


class Feature(AbstractFeature):
  def __init__(self, identifier, existencestarttime=None, existenceendtime=None,
          storetransactionstarttime=None, storetransactionendtime=None,
          name=None, value=None):
    self.__class__ = Feature
    super(Feature, self).__init__(identifier, existencestarttime, 
            existenceendtime, storetransactionstarttime, storetransactionendtime,
            name, value)
    self.validate();

  def validate(self):
    super(Feature, self).validate()

  def __str__(self):
    return str(self.identifier)


class FeatureList(list):
  def __init__(self, *args):
    super(FeatureList, self).__init__()
    for arg in args:
      self.append(arg)

  def append(self, feature):
    if not isinstance(feature,Feature):
      raise Exception("It's not a feature: " + str(feature))  
    super(FeatureList, self).append(feature) 

