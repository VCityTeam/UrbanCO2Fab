from feature import Feature, FeatureList
from abstractfeature import AbstractFeature
from enum import Enum
from dateutil.parser import parse
from validate import Validate

class TransactionType(Enum):
  INSERT = 1
  REPLACE = 2
  DELETE = 3

class Transaction(AbstractFeature):
  def __init__(self, identifier, existencestarttime=None, existenceendtime=None,
          storetransactionstarttime=None, storetransactionendtime=None,
          oldfeature=None, newfeature=None, transactiontype=None):
    super(Transaction, self).__init__(identifier, existencestarttime, 
            existenceendtime, storetransactionstarttime, storetransactionendtime,
            identifier+".transactions")
    Validate.validateclass(TransactionType, transactiontype)
    if (oldfeature is not None):
      Validate.validateclass(Feature, oldfeature)
    if (newfeature is not None):
      Validate.validateclass(Feature, newfeature)
    self.__class__ = Transaction
    self.oldfeature = oldfeature
    self.newfeature = newfeature
    self.transactiontype = transactiontype
    self.validate()

  def update(self, existencestarttime=None, existenceendtime=None):
    self.existenceendtime = None
    self.existencestarttime = None
    self.type = None

  def get(self, filters=[], info=dict()):
    super(Transaction, self).get(filters, info)
    for fter in filters:
      if (fter == "all"):
        info["oldfeature"] = self.oldfeature
        info["newfeature"] = self.newfeature
        break
      if (fter == "oldfeature"):
        info["oldfeature"] = self.oldfeature
      if (fter == "oldfeature"):
        info["newfeature"] = self.newfeature
    return info

  def validate(self):
    if (self.transactiontype == TransactionType.DELETE):
      if (self.oldfeature.__class__ != Feature):
        raise Exception("Old feature not of the correct type-" + str(self.oldfeature.__class__) + ": " + str(Feature))
        if(self.newfeature != None):
          raise Exception("New feature must be none, when transaction type is DELETE")
    if (self.transactiontype == TransactionType.INSERT):
      if (self.newfeature.__class__ != Feature):
        raise Exception("New feature not of the correct type-" + str(self.newfeature.__class__) + ": " + str(Feature))
        if(self.oldfeature != None):
          raise Exception("Old feature must be none, when transaction type is INSERT")
    if (self.transactiontype == TransactionType.REPLACE):
      if(self.newfeature.get(filters=
         ["name"])["name"] !=
        self.oldfeature.get(filters=
         ["name"])["name"]):
       raise Exception("Old feature and new feature name must be the same")
      if(self.newfeature.get(filters=
         ["value"])["value"] ==
        self.oldfeature.get(filters=
         ["value"])["value"]):
       raise Exception("Old feature and new feature value must not be the same")
      if(self.newfeature.get(filters=
         ["identifier"])["identifier"] !=
        self.oldfeature.get(filters=
         ["identifier"])["identifier"]):
        raise Exception("Old feature and same feature must have the same identifier")
      if(parse(self.newfeature.get(filters=
         ["existencestarttime"])["existencestarttime"]) <
        parse(self.oldfeature.get(filters=
         ["existenceendtime"])["existenceendtime"])):
        raise Exception("End time of old feature must be less than the start time of the old feature")

class TransactionList(list):
  def __init__(self, *args):
    super(TransactionList, self).__init__()
    self.__class__ == TransactionList
    for arg in args:
      self.append(arg)

  def append(self, transaction):
    if not isinstance(transaction,Transaction):
      raise Exception("It's not a transaction: " + str(transaction))  
    super(TransactionList, self).append(transaction) 

