//import * as vis from 'vis-network';

import { get_data_and_options } from "./json_parser";

class NetworkManagerSingleton {
    constructor(start_mode="default", id_network="mynetwork", id_button_location="mybuttons"){
    /**
     * Constructor for singleton
     */
        console.log(1);
        const instance = this.constructor.instance;
        console.log(1);
        if(instance){
            return instance;
        }
        else{
            console.log(1);
            this.network = null;
            this.data = null;
            this.list_option = null;
            this.current_mode = start_mode;
            this.id_network = id_network;
            this.id_button_location = id_button_location;
            this.constructor.instance = this;
        }

    }

    destroy() {
    /**
     * Kill the simulation network  
     */
        if (this.network !== null) {
            console.info("Network destroyed");
          this.network.destroy();
          this.network = null;
        }
    }

    init_from_json_path(json_data_path, json_options_path){
        console.log("NetworkManager init from json data: %s || options: %s", json_data_path, json_options_path);
        this.data = get_data_and_options(json_data_path).data;
        this.list_option = get_data_and_options(json_options_path).list_options;
        this.add_button_to_view();
    }

    get_option(mode){
    /**
     * Extract the matching options to a specific mode from the list_option
     * /!\ Working specificaly with vis.network
     * @param mode specific mode correspondong to a specific view
     * @return ready to used json for vis-network
     */
        console.log("Get option : %s", mode);
        var test = mode;
        if (mode === "default"){
            test = undefined
        }
        console.log(1);
        for (const key in this.list_option) {
            console.log(1);
            if (this.list_option.hasOwnProperty(key)) {
                console.log(1);
                const element = this.list_option[key];
                if (test === element.label){
                    console.log(2);
                    return element.option.viz
                }
            }
        }
        return this.list_option[0].option.viz;
    }

    add_button_to_view(){
    /**
     * Add button to navigate between view. There will be one button by options present in list_option
     * onClick will be a draw()
     */
        console.log("Try to add %s button(s)", this.list_option.length.toString());
        for (const key in this.list_option) {
            if (this.list_option.hasOwnProperty(key)) {
                const option = this.list_option[key];

                var button = document.createElement("button");

                const new_label = option.label === undefined ? "default" : option.label;
                console.log("Creating button with label : %s", new_label.toString());
                var label = document.createTextNode(new_label.toString());
                button.appendChild(label);

                button.onclick = function (param) {
                    console.log("Button %s clicked : %o", param.target.innerText, param);
                    n.draw(param.target.innerText);
                };

                var element = document.getElementById(this.id_button_location);
                element.insertBefore(button, mode);

                console.info("Button added : %s", mode.value);
            }
        }
    }

    draw(mode="default") {
    /**
     * Draw the network inside the client page
     */
        this.current_mode = mode;
        this.destroy();  
    
        if (this.data === null){
            this.data = get_data_and_options(json_path).data;
        }
        if (this.list_option === null){
            this.list_option = get_data_and_options(json_path).list_options;
            this.add_button_to_view();
        }
    
        const options = this.get_option(this.current_mode);
        const container = document.getElementById(this.id_network);
        console.log("Drawing Container : %o Data : %o Options : %o", container, this.data, options);
        var network = new vis.Network(container, this.data, options);
        console.info("Network drawn");
        console.log(network);
        }
}

// test
const json_data_path = __dirname + "/input/urban_data.json";
const json_options_path = __dirname + "/input/urban_option.json";
console.log("path");
window.addEventListener("load", () => {
    console.log(__dirname);
    var n = new NetworkManagerSingleton();
    n.init_from_json_path(json_data_path, json_options_path);
    //n.draw();
    });