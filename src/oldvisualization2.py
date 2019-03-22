import webbrowser
import json
from shutil import copyfile

vizfilename = "/tmp/index.html"

start = '''
<html>
 <head>
  <title>UrbanCo2Fab Visualization</title>
  <link rel="stylesheet" type="text/css" href="gitgraph.css" />
  <script src="gitgraph.min.js"></script>
 </head>
 <body>
  <canvas id="gitGraph"></canvas>
  <script>
   var gitgraph = new GitGraph({
     template: "metro",
     orientation: "horizontal",
     mode: "compact"
   });
'''
end = '''
  </script>
 </body>
</html>
'''

gitgraphcode = ''

def create_viz():
  with open(vizfilename, "w") as vizfile:
    copyfile("./gitgraph.min.js", "/tmp/gitgraph.min.js")
    copyfile("./gitgraph.css", "/tmp/gitgraph.css")
    with open("workspace.json") as jsonfile:
      workspace = json.load(jsonfile)
      with open("scenarios.json") as jsonfile:
        scenarios = json.load(jsonfile)
      print(workspace["consensus"])
      gitgraphcode = '''
      var consensus = gitgraph.branch("consensus");
      '''
      consensusversionset = set()
      propositioncount = 0
      split = False
      for count in range(len(scenarios[workspace["consensus"]]["versions"])):
        consensusversion = scenarios[workspace["consensus"]]["versions"][count]
        for scenario in workspace["propositions"]:
          propositioncount = propositioncount + 1
          if consensusversion == scenarios[scenario]["versions"][0]:
            gitgraphcode = gitgraphcode + '\nproposition' +  str(propositioncount) + ' = consensus.branch("proposition' +  str(propositioncount) + '");'
          else:
            if consensusversion not in consensusversionset:
              if(split is not False):
                gitgraphcode = gitgraphcode + '\nconsensus.commit("' +  consensusversion + '");'
                consensusversionset.add(consensusversion)
        for scenario in workspace["propositions"]:
          for version in scenarios[scenario]["versions"]:
            gitgraphcode = gitgraphcode + "\nproposition" +  str(propositioncount) +'.commit("' +  version + '");'
          gitgraphcode = gitgraphcode + '\nconsensus.merge(proposition' +  str(propositioncount) + ")"
      print(gitgraphcode)
         
      print(workspace["propositions"])
      for scenario in workspace["propositions"]:
        print(scenarios[scenario]["versions"][0])
    
    contents = start + gitgraphcode + end
    vizfile.write(contents)      
    vizfile.close()
    

def show():
  create_viz()
  webbrowser.open(vizfilename)
