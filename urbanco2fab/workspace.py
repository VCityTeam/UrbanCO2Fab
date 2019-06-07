import error
import sys
import version
import json
import scenario
from shutil import copyfile
from pygit2 import Repository, credentials
from datetime import datetime, timezone, timedelta
from abstractfeature import AbstractFeature
from scenario import *
from validate import Validate
from enum import Enum

class Workspace(AbstractFeature):
  def __init__(self, identifier, existencestarttime=None, existenceendtime=None,
          storetransactionstarttime=None, storetransactionendtime=None,
          title=None, description=None,tags=None,
          consensusscenario=None, propositionscenarios=None, userid=None):
    super(Workspace, self).__init__(identifier, existencestarttime, 
            existenceendtime, storetransactionstarttime, storetransactionendtime,
            identifier+".workspace")
    self.__class__ = Workspace
    self.description = description
    self.tags = tags
    self.title = title
    self.consensusscenario = consensusscenario
    self.propositionscenarios = propositionscenarios
    self.userid = userid
    self.validate()

  def validate(self):
    Validate.validateclass(Scenario, self.consensusscenario)
    if(self.propositionscenarios is not None):
      Validate.validateclass(ScenarioList, self.propositionscenarios)

  def get(self, filters=[], info=dict()):
    super(Transaction, self).get(filters, info)
    for fter in filters:
      if (fter == "all"):
        info["consensusscenario"] = self.consensusscenario
        info["propositionscenarios"] = self.propositionscenarios
        info["title"] = self.title
        info["description"] = self.description
        info["tags"] = self.tags
        info["userid"] = self.userid
        break
      if (fter == "description"):
        info["description"] = self.description
      if (fter == "userid"):
        info["userid"] = self.userid
      if (fter == "tags"):
        info["tags"] = self.tags
      if (fter == "title"):
        info["title"] = self.title
      if (fter == "propositionscenarios"):
        info["propositionscenarios"] = self.propositionscenarios
      if (fter == "consensusscenario"):
        info["consensusscenario"] = self.consensusscenario
    return info

