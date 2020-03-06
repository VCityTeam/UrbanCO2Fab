import * as fs from 'fs';

function get_graph_from_json_file(json_path) {
/**
 * Read and parse a json file
 * @returns json parsed object 
 * */    
    var ret = null

    var data = fs.readFileSync(json_path);
    console.log("JSON read at : %s", json_path);
    ret = JSON.parse(data);
    console.log("JSON parsed : %s", JSON.stringify(ret));
    return ret;
}

module.exports = {
    get_graph_from_json_file: function(json_path) {
        return get_graph_from_json_file(json_path);
    }
};

// test
get_graph_from_json_file('input/urban_graph.json');