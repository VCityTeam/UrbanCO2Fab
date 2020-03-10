//import * as fs from 'fs';

export function get_graph_from_json_file(json_path) {
/**
 * Read and parse a json file
 * @returns json parsed object 
 * */    
/*
    var ret = null

    var data = fs.readFileSync(json_path);
    console.log("JSON read at : %s", json_path);
    ret = JSON.parse(data);
    console.log("JSON parsed : %s", JSON.stringify(ret));
    return ret;
*/
    var ret = {
        nodes: [
              {
                id: 0,
                label: "2000",
                level: 0,
                group: "timeFrame"
            },
            {
                id: 1,
                label: "2001",
                level: 1,
                group: "timeFrame"
            },
            {
                id: 2,
                label: "2002",
                level: 2,
                group: "timeFrame"
            },
            {
                id: 3,
                label: "2003",
                level: 3,
                group: "timeFrame"
            },
            {
                id: 4,
                label: "2004",
                level: 4,
                group: "timeFrame"
            },
            {
                id: 5,
                label: "2005",
                level: 5,
                group: "timeFrame"
            },
            {
                id: 6,
                label: "C_2000",
                level: 0,
                group: "consensusScenario"
            },
            {
                id: 7,
                label: "C_2002",
                level: 2,
                group: "consensusScenario"
            },
            {
                id: 8,
                label: "C_2004",
                level: 4,
                group: "consensusScenario"
            },
            {
                id: 9,
                label: "P_2001",
                level: 1,
                group: "propositionScenario"
            },
            {
                id: 10,
                label: "P_2001",
                level: 1,
                group: "propositionScenario"
            },
            {
                id: 11,
                label: "P_2004",
                level: 4,
                group: "propositionScenario"
            },
            {
                id: 12,
                label: "C_2004-2",
                level: 4,
                group: "consensusScenario"
            }
        ],
        edges: [
              {
                from: 0,
                to: 1
            },
            {
                from: 1,
                to: 2
            },
            {
                from: 2,
                to: 3
            },
            {
                from: 3,
                to: 4
            },
            {
                from: 4,
                to: 5
            },
            {
                from: 6,
                to: 7,
                color: "red",
                label: "modification"
            },
            {
                from: 7,
                to: 8,
                color: "blue",
                label: "split"
            },
            {
                from: 7,
                to: 12,
                color: "blue",
                label: "split"
            },
            {
                from: 9,
                to: 7,
                color: "green",
                label: "merge"
            },
            {
                from: 10,
                to: 7,
                color: "green",
                label: "merge"
            },
            {
                from: 7,
                to: 11,
                color: "black",
                label: "destruction"
            }
    
        ],
        options:
        [
            {
                viz:
                {
                    edges: 
                            {
                                smooth: 
                                {
                                    type: "cubicBezier"
                                },
                                arrows: { to: true },
                                font:{ align: "middle"},
                                length:170
                            },
                    groups:
                            {
                                useDefaultGroups: true,
                                timeFrame:{
                                    //id: 0,
                                    color: "white",
                                    hidden: "true",
                                    //label: "Time legend"
                                },
                                consensusScenario:{
                                    //id: 1,
                                    color: "green",
                                    //label: "Consensus scenario"
                                },
                                propositionScenario:{
                                    //id: 2,
                                    color: "yellow",
                                    //label: "Proposition scenario"
                                }
                            },
                    physics:
                            {
                                stabilization: true,
                                //wind: { x: 0, y: 0 }
                            }
                }
                
            },
            {
                mode:"hierarchy",
                viz:{
                    edges: 
                    {
                        smooth: 
                        {
                            type: "cubicBezier"
                        },
                        arrows: { to: true },
                        font:{ align: "middle"},
                        length:170
                    },
                    groups:
                    {
                        useDefaultGroups: true,
                        timeFrame:{
                            color: "white",
                            hidden: false,
                            physics: false,
                            //id: 0,
                            //mode: "hierarchy",
                            //label: "Time legend"
                        },
                        consensusScenario:{
                            //id: 1,
                            color: "green",
                            //label: "Consensus scenario"
                        },
                        propositionScenario:{
                            //id: 2,
                            color: "yellow",
                            //label: "Proposition scenario"
                        }
                    },
                    layout: 
                    {
                        hierarchical: 
                        {
                            direction: "LR",
                            sortMethod: "directed",
                            treeSpacing: 100,
                            parentCentralization: false
                        },
                        randomSeed: 2
                    },
                    interaction: { 
                        dragNodes: false,
                        dragView: false,
                        hover: true,
                        zoomView: false

                    },
                    physics: 
                    {
                    enabled: true,
                    }
                }
            }
        ]
    }

    return ret;

}

// test
get_graph_from_json_file('input/urban_graph.json');