import * as vis from 'vis-network';

import * as json_manager from "json_parser";


var network = null;
var data = null;
var list_options = null;
var mode = document.getElementById("mode");


function destroy() {
    if (network !== null) {
      network.destroy();
      network = null;
    }
  }

function draw(json_path, id_network="mynetwork", id_button_location="mybutton") {
    destroy();

    if (data === null){
        data = json_manager.get_data(json_path);
    }
    if (list_options === null){
        list_options = json_manager.get_list_options(json_path);
        
        // add button for each mode
        for (const key in list_options) {
            if (list_options.hasOwnProperty(key)) {
                const option = list_options[key];
                
                const mode = option.label;
                var button = document.createElement("button");
                var label = document.createTextNode(mode.toString());
                button.appendChild(label);
                button.onclick = function (param) {
                    console.log("Clicked : %s", param);
                    console.log(label);                    
                };

                var element = document.getElementById("mybutton");
                element.insertBefore(button);

                console.info("Button added : %s", mode);
            }
        }
    }

    options = list_options[0];
    var container = document.getElementById(id_network);

    var network = new vis.Network(container, data, options);
    }



// test
const json_path = __dirname + '/input/urban_graph.json';

window.addEventListener("load", () => {
    console.log(__dirname);
    draw(json_path);
    });