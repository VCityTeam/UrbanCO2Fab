//import * as vis from 'vis-network';

import { get_data, get_list_options } from "./json_parser";

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

    init(url_data="http://localhost:5000/urban_data1.json", url_option="http://localhost:5000/urban_option1.json"){
        console.log("NetworkManager init from url data: %s || options: %s", url_data, url_option);
        this.prepare_html_pages(url_data, url_option);
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
                    var n = new NetworkManagerSingleton ();
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
    
        const options = this.get_option(this.current_mode);
        const container = document.getElementById(this.id_network);
        console.log("Drawing Container : %o Data : %o Options : %o", container, this.data, options);
        var network = new vis.Network(container, this.data, options);
        console.info("Network drawn");
        console.log(network);
    }

    prepare_html_pages(data_url, data_option) {
        var button_load = document.getElementById("getData");
        button_load.onclick = function(param) {
            var n = new NetworkManagerSingleton();

            var request_d = new XMLHttpRequest();
            var result_d = null;
            request_d.open("GET", data_url);
            console.log("GET Request to %s", data_url.toString());
            request_d.onreadystatechange = function() {
                if(this.readyState === 4 && this.status === 200) {
                    result_d = JSON.parse(this.responseText);
                    console.log("result data: %o", result_d);
                    n.data = get_data(result_d);
                }
            };
            request_d.send();

            var request_o = new XMLHttpRequest();
            var result_o = null;
            request_o.open("GET", data_option);
            console.log("GET Request to %s", data_option.toString());
            request_o.onreadystatechange = function() {
                if(this.readyState === 4 && this.status === 200) {
                    result_o = JSON.parse(this.responseText);
                    console.log("result option: %o", result_o);
                    n.list_option = get_list_options(result_o);
                }
            };
            request_o.send();


        }
    }
}

// test
console.log("path");
window.addEventListener("load", () => {
    console.log(__dirname);
    var n = new NetworkManagerSingleton();
    n.init();
    //n.draw();
    });