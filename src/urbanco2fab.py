import argparse
import scenario
import version
import datetime
import versiontransition
from dateutil.parser import parse

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


parser.add_argument("-r", "--repository", nargs=1, help="repository")
parser.add_argument("-t", "--title", nargs=1, help="title of scenario")
parser.add_argument("-e", "--document", nargs='+', help="one or more document evidences")
parser.add_argument("-m", "--time", nargs='+', help="one or more times")
parser.add_argument("-d", "--description", nargs=1, help="description of scenario")
parser.add_argument("-s", "--scenario", nargs='+', help="scenario related operations")
parser.add_argument("-v", "--version", nargs='+', help="versions (or commit identifiers) version:type:label, where type can be Existing or Imagined and label can be a string of characters using single or double quotes")
parser.add_argument("-vt", "--versiontransition", nargs='+', help="list of pairs of versions (or commit identifiers) version1:version2:type:label, where type can be Regular or Influence and label can be a string of characters using single or double quotes")
parser.add_argument('operation', help="operation to perform",
          type=str, choices=['add', 'mv', 'rm', 'commit', 'show', 'tag', 'log', 'diff',
                             'clone', 'init', 'fetch', 'pull', 'push',
                             'checkout'])
args = parser.parse_args()

if (args.operation == "show"):
  if (args.scenario is not None):
    scenario.get_scenario(args.scenario)
  elif (args.version is not None):
    version.get_version(args.version)
  elif (args.versiontransition is not None):
    versiontransition.get_versiontransition(args.versiontransition)
  elif (args.historical == "historical"):
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
  if (args.scenario is not None):
    if (args.version is not None  and args.versiontransition is not None 
          and args.repository is not None and args.title is not None 
          and args.description is not None):
      scenario.create_scenario(args.repository[0], args.version, 
           args.versiontransition, args.title[0], args.description[0])
    else:
       print(parser.print_help())
  else:
    print(parser.print_help())
else:
  print(parser.print_help())
