from abstractfeature import AbstractFeature


class Feature(AbstractFeature):
  def __init__(self, identifier, existencestarttime=None, existenceendtime=None,
          storetransactionstarttime=None, storetransactionendtime=None,
          name=None, value=None):
    super(Feature, self).__init__(identifier, existencestarttime, 
            existenceendtime, storetransactionstarttime, storetransactionendtime,
            name)
    self.__class__ = Feature
    self.value=value
    self.validate();

  def validate(self):
    super(Feature, self).validate()

  def get(self, filters=[], info=dict()):
    super(Feature, self).get(filters, info)
    for fter in filters:
      if (fter == "all"):
        info["value"] = self.value
      if (fter == "value"):
          info["value"] = self.value
    return(info)

  def __str__(self):
    return str(self.identifier)


class FeatureList(list):
  def __init__(self, *args):
    super(FeatureList, self).__init__()
    self.__class__ = FeatureList
    for arg in args:
      self.append(arg)

  def append(self, feature):
    if not isinstance(feature,Feature):
      raise Exception("It's not a feature: " + str(feature))  
    super(FeatureList, self).append(feature) 

