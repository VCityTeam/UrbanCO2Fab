import webbrowser
import json
from shutil import copyfile

vizfilename = "/tmp/index.html"

start = '''
<html>
 <head>
  <title>UrbanCo2Fab Visualization</title>
  <script src="viz.js"></script>
  <script src="full.render.js"></script>
  <script>
  function loadDotGraph() {
    var viz = new Viz();
  
    viz.renderSVGElement(`digraph { 
      graph [
        splines=ortho; 
      ];
       rankdir=LR;
'''
end = '''
      }`)
      .then(function(element) {
       document.body.appendChild(element);
    })
    .catch(error => {
      // Create a new Viz instance (@see Caveats page for more info)
      viz = new Viz();

      // Possibly display the error
      console.error(error);
    });
   }
  </script>
 </head>
 <body onload="loadDotGraph()">
 </body>
</html>
'''

gitgraphcode = ""

def create_viz():
  with open(vizfilename, "w") as vizfile:
    copyfile(".urbanco2fab/viz.js", "/tmp/viz.js")
    copyfile(".urbanco2fab/full.render.js", "/tmp/full.render.js")
    with open(".urbanco2fab/workspace.json") as jsonfile:
      workspace = json.load(jsonfile)
      with open(".urbanco2fab/scenarios.json") as jsonfile:
        scenarios = json.load(jsonfile)
      gitgraphcode = ""
      gitgraphcode = gitgraphcode + '''
	subgraph cluster_0 {
		style=filled;
		color=lightgrey;
		node [style=filled,color=white];
		edge [
         arrowhead="none"
        ];
        arrowhead=none;
        label="consensus:'''+scenarios[workspace["consensus"]]["title"] + '''";'''
      versionshort = [v[:6] for v in scenarios[workspace["consensus"]]["versions"]]
      #gitgraphcode = gitgraphcode +'"'+ '"->"'.join(scenarios[workspace["consensus"]]["versions"])+ '"'
      gitgraphcode = gitgraphcode +'"'+ '"->"'.join(versionshort)+'"'
      gitgraphcode = gitgraphcode + ''';
        }
      '''
      
      for scenario in workspace["propositions"]:
        gitgraphcode = gitgraphcode + '''
	  subgraph cluster_''' + scenario+ '''{
            node [style=filled];
	    edge [
              arrowhead="none"
            ];
            label="''' + scenario + '''";
        '''
        versionshort = [v[:6] for v in scenarios[scenario]["versions"]]
        #gitgraphcode = gitgraphcode +'"'+ '"->"'.join(scenarios[scenario]["versions"])+'"'
        gitgraphcode = gitgraphcode +'"'+ '"->"'.join(versionshort)+'"'
        gitgraphcode = gitgraphcode + ''';
        }
        '''
    
    contents = start + gitgraphcode + end
    vizfile.write(contents)      
    vizfile.close()
    

def show():
  create_viz()
  webbrowser.open(vizfilename)
