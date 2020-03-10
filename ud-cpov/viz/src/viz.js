import * as vis from 'vis-network';

import { get_data_and_options } from "./json_parser";


var network = null;
var data = null;
var list_options = null;
var mode = document.getElementById("mode");


function destroy() {
    if (network !== null) {
        console.info("Network destroyed");
      network.destroy();
      network = null;
    }
  }

function get_option(list_options, mode){
    console.log("Get option : %s", mode);
    var test = mode;
    if (mode === "default"){
        test = undefined
    }
    for (const key in list_options) {
        if (list_options.hasOwnProperty(key)) {
            const element = list_options[key];
            if (test === element.label){
                return element.option
            }
        }
    }
    return list_options[0].option;
}

function draw(json_path, id_network="mynetwork", id_button_location="mybutton") {
    destroy();
    var mode = document.getElementById("mode");


    if (data === null){
        data = get_data_and_options(json_path).data;
    }
    if (list_options === null){
        list_options = get_data_and_options(json_path).list_options;
        
        // add button for each mode
        console.log("Try to add %s button(s)", list_options.length.toString());
        for (const key in list_options) {
            if (list_options.hasOwnProperty(key)) {
                const option = list_options[key];

                var button = document.createElement("button");

                const new_label = option.label === undefined ? "default" : option.label;
                console.log("Creating button with label : %s", new_label.toString());
                var label = document.createTextNode(new_label.toString());
                button.appendChild(label);
                button.onclick = function (param) {
                    console.log("Button %s clicked : %o", param.target.innerText, param);
                    mode.value = param.target.innerText;
                    draw('');
                };

                var element = document.getElementById("mybuttons");
                element.insertBefore(button, mode);

                console.info("Button added : %s", mode.value);
            }
        }
    }

    //var options = list_options[0].option;
    var options = get_option(list_options, mode.value)
    var container = document.getElementById(id_network);
    console.log("Drawing Container : %o Data : %o Options : %o", container, data, options.viz);
    var network = new vis.Network(container, data, options.viz);
    console.info("Network drawn");
    console.log(network);
    }



// test
const json_path = __dirname + '/input/urban_graph.json';

window.addEventListener("load", () => {
    console.log(__dirname);
    draw(json_path);
    });