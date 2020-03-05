import argparse
import visualization
import scenario
import version
import diff
import os
import os
import datetime
import versiontransition
import datetime
from objects.workspace import Workspace
from dateformat.dateformat import DateFormatAction
from store.storefactory import StoreFactory

parser = argparse.ArgumentParser(description="management of city data")
versiongroup = parser.add_argument_group('version', "management of versions")
transitiongroup = parser.add_argument_group('transition', "management of transitions")
transactiongroup = parser.add_argument_group('transaction', "management of transactions")
scenariogroup = parser.add_argument_group('scenario', "management of scenarios")
workspacegroup = parser.add_argument_group('workspace', "management of workspaces" )

versiongroup.add_argument("-vtp", '--versiontype', help="type of transitions",
          type=str, choices=['existing', 'imagined'], required=False)

transitiongroup.add_argument("-hs", '--historical', help="historical log",
          required=False, const='historical', action='store_const')
transitiongroup.add_argument("-fu", '--future', help="future log",
          required=False, const="future", action='store_const')
transitiongroup.add_argument("-tp", '--transitiontype', help="type of transitions",
          type=str, choices=['regular', 'influence'])

scenariogroup.add_argument("-st", '--scenariotype', help="type of scenario",
          type=str, choices=['consensus', 'proposition'])


parser.add_argument("-b", '--bare', help="bare repository", const='bare',
                     required=False, action='store_const')
parser.add_argument("-w", "--workspace", nargs=1, help="workspace")
parser.add_argument("-g", "--tag", nargs='+', help="tag")
parser.add_argument("-f", "--graph", nargs='+', help="difference graph, if available between versions")
parser.add_argument("-e", "--document", nargs='+', help="one or more document evidences")
parser.add_argument("-r", "--source", nargs='+', help="source of a given file(s)")
parser.add_argument("-m", "--message", nargs='+', help="message")
parser.add_argument("-i", "--time", nargs='+', help="one or more times", action=DateFormatAction)
parser.add_argument("-d", "--description", nargs=1, help="description of scenario")
parser.add_argument("-s", "--scenario", nargs='+', help="scenario related operations")
parser.add_argument("-c", "--consensus", nargs=1, help="consensus scenario")
parser.add_argument("-l", "--influence", nargs=1, help="influence between versions, v1:v2")
parser.add_argument("-p", "--proposition", nargs='+', help="proposition scenarios")
parser.add_argument("-v", "--version", nargs='+', help="versions (or commit identifiers) version:type:label, where type can be Existing or Imagined and label can be a string of characters using single or double quotes")
parser.add_argument("-vt", "--versiontransition", nargs='+', help="list of pairs of versions (or commit identifiers) version1:version2:type:label, where type can be Regular or Influence and label can be a string of characters using single or double quotes")
parser.add_argument('operation', help="operation to perform",
          type=str, choices=['add', 'mv', 'rm', 'commit', 'show', 'tag', 'log', 'diff',
                             'clone', 'init', 'fetch', 'pull', 'push', 'viz',
                             'checkout'])
parser.add_argument('path', help="path of files", nargs='*')
parser.add_argument('arguments', metavar='A', type=str, nargs='*',
                    help='option to arguments')
args = parser.parse_args()

if (args.operation == "show"):
  if (args.scenario is not None):
    scenario.get_scenario(' '.join(args.scenario))
  elif (args.version is not None):
    if(args.version[0] == 'all'):
      version.get_all()
    else:
      version.get_version(args.version)
  elif (args.versiontransition is not None):
    versiontransition.get_versiontransition(args.versiontransition)
  else:
    Workspace.get_workspace()
elif (args.operation == "log"):
  if (args.historical == "historical"):
    if(args.time is None):
      version.get_version_wrt_time(True, datetime.datetime.now(datetime.timezone.utc))
    else:
      version.get_version_wrt_time(True, parse(args.time[0]))
  elif (args.future == "future"):
    if(args.time is None):
      version.get_version_wrt_time(False, datetime.datetime.now(datetime.timezone.utc))
    else:
      version.get_version_wrt_time(False, parse(args.time[0]))
elif (args.operation == "add"):
  if (args.workspace is None):
    cwd = os.getcwd()
    Workspace.add(cwd, args.path)
  else:
    cwd = os.getcwd()
    Workspace.add(cwd)
elif (args.operation == "pull"):
  if (args.workspace is not None) :
    Workspace.pull(args.workspace[0])
  else:
    cwd = os.getcwd()
    Workspace.pull(cwd)
elif (args.operation == "push"):
  if (args.workspace is not None) :
    Workspace.push(args.workspace[0])
  else:
    cwd = os.getcwd()
    Workspace.push(cwd)
elif (args.operation == "init"):
  bare = False
  if (args.bare is not None):
    bare = True
  if (args.path is not None):
    Workspace(args.path[0], bare, datetime.datetime.now(datetime.timezone.utc))
  elif (len(args.arguments) > 0):
    Workspace(args.arguments[0], bare)
  else:
    cwd = os.getcwd()
    Workspace(cwd, bare)
elif (args.operation == "rm"):
  workspacepath = os.getcwd()
  if (args.workspace is not None) :
    workspacepath = args.workspace[0] 
  Workspace.rm(workspacepath, args.path)
elif (args.operation == "mv"):
  workspacepath = os.getcwd()
  if (args.workspace is not None) :
    workspacepath = args.workspace[0] 
  Workspace.move(workspacepath, args.path)
elif (args.operation == "commit"):
  workspacepath = os.getcwd()
  description = ""
  source = []
  versiontype = "existing"
  tag = []
  document = []
  if (args.description is not None):
    description = ' '.join(args.description)
  if (args.tag is not None):
    tag = args.tag
  if (args.source is not None) :
    source = args.source
  if (args.document is not None) :
    document = args.document
  if (args.versiontype is not None) :
    versiontype = args.versiontype
  if (args.workspace is not None) :
    workspacepath = args.workspace[0] 
  scenariotype = "proposition"
  if(args.scenariotype is not None):
    scenariotype = args.scenariotype[0]
  if (args.consensus is not None or args.proposition is not None):
    consensus = []
    propositions = []
    influence = []
    if (args.consensus is not None):
      consensus = args.consensus
    if (args.proposition is not None):
      proposition = args.proposition
    if (args.influence is not None):
      influence = args.influence
    Workspace.create_workspace(workspacepath, consensus, proposition, influence)
    exit(1)
  if (args.scenario is not None):
    if (args.version is None or args.versiontransition is None):
      print("usage: urbanco2fab commit -s 'scenario name' --version v1 v2' "+
             "--versiontransition v1-v2 [--graph file+]")
      exit(1)
    if (args.version is not None  and args.versiontransition is not None):
      if (args.graph is not None):
        scenario.create_scenario(workspacepath, args.version, 
           args.versiontransition, ' '.join(args.scenario), description, args.graph)
      else:
        scenario.create_scenario(workspacepath, args.version, 
           args.versiontransition, ' '.join(args.scenario), description)
    exit(1)
  if (args.time is None):
    print("usage: urbanco2fab commit -m 'message' --time 't1,t2' ")
    exit(1)
  else:
    timelist = args.time[0].split(",")
    if(len(timelist)!=2):
      print("usage: urbanco2fab commit -m 'message' --time 't1,t2' ")
      exit(1)
    starttime = timelist[0]
    endtime = timelist[1]
  if (args.message is not None):
    workspace.commit(workspacepath, ' '.join(args.message), starttime, endtime,
         description, tag, document, versiontype, source)
  else:
    print("Commit message is empty")
elif (args.operation == "tag"):
  workspacepath = os.getcwd()
  if (args.workspace is not None) :
    workspacepath = args.workspace[0] 
  if (args.message is not None):
    if (args.version is not None):
      version.tag(workspacepath, args.version[0], args.message)
    elif (args.scenario is not None):
      if (args.versiontransition is not None):
        versiontransition.tag(workspacepath, ' '.join(args.scenario), 
           args.versiontransition[0], args.message)
      else:
        scenario.tag(workspacepath, ' '.join(args.scenario), args.message)
  else:
    print("Commit message or scenario is empty")
elif (args.operation == "clone"):
  bare = False
  if (args.bare is not None):
    bare = True
  workspace_name = None
  if (len(args.path)>0):
    workspace_name = args.path[0] 
  if (args.workspace is not None) :
    workspace_name = args.workspace[0]
  if (workspace_name == None):
    print("Check the workspace")
  else:
    if (args.path is not None and len(args.path) > 1):
      workspace.clone(workspace_name, args.path[1], bare)
    else:
      cwd = os.getcwd()
      workspace.clone(workspace_name, cwd, bare)
elif (args.operation == "diff"):
  if (len(args.path) == 2):
    workspacepath = os.getcwd()
    diff.get_transactions(workspacepath, args.path[0], 
        args.path[1], display=True)
  else:
    print("Diff takes two arguments, given "+ str(len(args.path)))
elif (args.operation == "viz"):
  visualization.show()
else:
  print(parser.print_help())
