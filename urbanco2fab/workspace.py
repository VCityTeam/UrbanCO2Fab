from error import *
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
  def __init__(self, identifier, bare, storetransactionstarttime,
          storetransactionendtime=None, title=None, description=None,tags=None,
          consensusscenario=None, propositionscenarios=None, userid=None):
    self.__class__ = Workspace
    self.description = description
    self.tags = tags
    self.title = title
    self.consensusscenario = consensusscenario
    self.propositionscenarios = propositionscenarios
    self.userid = userid
    self.validate()

  def validate(self):
    if(self.consensusscenario is not None):
      Validate.validateclass(Scenario, self.consensusscenario)
    if(self.propositionscenarios is not None):
      Validate.validateclass(ScenarioList, self.propositionscenarios)
    """
      There's at least one common version between consensus
      and proposition scenarios. We check the identifier of the identifier
    """
    if self.propositionscenarios is not None:
      csversionset = set()
      for version in self.consensusscenario.get(filters=["versions"])["versions"]:
        csversionset.add(version.get(filters=["identifier"])["identifier"])
      
      commonversion = False
      for pscenario in self.propositionscenarios:
        for version in self.consensusscenario.get(filters=["versions"])["versions"]:
           if(version.get(filters=["identifier"])["identifier"] in csversionset):
              commonversion = True
  
      if (not commonversion):
        raise(ConsensusScenarioError("There must be at least one common version between consensus and proposition scenarios"))

    """
      All the version types in a Consensus scenario must be of type 'Existing'.
    """
    if (self.consensusscenario is not None): 
      for version in self.consensusscenario.get(filters=["versions"])["versions"]:
        if (version.get(filters=["type"])["type"] != VersionType.EXISTING):
          raise(ConsensusScenarioError("All version types in a consensus scenario must be of type existing"))

    """
      Consensus scenario and proposition scenarios must be disjoint
    """
    if self.propositionscenarios is not None:
      for pscenario in self.propositionscenarios:
        if(pscenario.get(filters=["identifier"])["identifier"] ==
            self.consensusscenario.get(filters=["identifier"])["identifier"]):
          raise(ConsensusScenarioError("Consensus scenario and proposition scenarios must be disjoint"))

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

