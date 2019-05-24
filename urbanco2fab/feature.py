class Feature(object):
  def __init__(self, identifier):
    self.__class__ = Transaction
    self.identifier = identifier

class FeatureList(list):
  def __init__(self, *args):
    super(FeatureList, self).__init__()
    for arg in args:
      self.append(arg)

  def append(self, feature):
    if not isinstance(feature,Feature):
      raise Exception("It's not a feature: " + str(feature))  
    super(FeatureList, self).append(feature) 

