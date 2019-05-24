from feature import Feature, FeatureList
from abstractfeature import AbstractFeature

class Transaction(AbstractFeature):
  def __init__(self, identifier, existencestarttime=None, existenceendtime=None,
          storetransactionstarttime=None, storetransactionendtime=None,
          featurelist=None):
    super(Transaction, self).__init__(identifier, existencestarttime, 
            existenceendtime, storetransactionstarttime, storetransactionendtime,
            identifier+".transactions")
    if (featurelist.__class__ != FeatureList):
      raise Exception("Feature list is not of the correct type-" + str(featurelist.__class__) + ": " + str(FeatureList))
    self.featurelist = featurelist
    self.validate()

  def update(self, existencestarttime=None, existenceendtime=None):
    self.existenceendtime = None
    self.existencestarttime = None
    self.type = None

  def get(self, filters=[]):
    return transactions

  def validate(self):
    for feature in self.features:
      if(parse(self.existencestarttime) == (feature.existencestarttime)):
        raise Exception("All the features must have the same start time as the transaction start time")
      if(parse(self.existenceendtime) == (feature.existenceendtime)):
        raise Exception("All the features must have the same end time as the transaction end time")

class TransactionList(list):
  def __init__(self, *args):
    super(TransactionList, self).__init__()
    for arg in args:
      self.append(arg)

  def append(self, transaction):
    if not isinstance(transaction,Transaction):
      raise Exception("It's not a transaction: " + str(transaction))  
    super(TransactionList, self).append(transaction) 

