# UD-CPOV.Viz 
## Intro :
This is a tool to visualize graphs in a web browser. Serving by an Express (Node.js) server and based on [vis.js](https://almende.github.io/vis/)

## Make it work :
### Installation :
* Copy the git repository
* Install the dependency with `npm install` in UrbanCO2Fab\ud-cpov\viz
* Start the server with `npm start`

You can now go on rou web browser in localhost:5000/graph.html to see an exemple.

### Try with your own data :
#### data.json :
You need to provide the data for the graph. It's a JSON file with the following format :
```
{
    "nodes": [
        {
            "id": int,          -- mandatory | Used to identify the node
            "label": string,    -- mandatory | Will be displayed in the graph on the node
            "level": int,       -- optional (but mandatory if a hierarchical view is wanted) | All same level will be in the same hierarchy
            "group": int        -- optional | Used for group options
        }, ...
    ],
    "edges": [
        {
            "from": int,        -- mandatory | from which node the edges should go
            "to": int,          -- mandatory | To which node the edges should go
            "color": string,    -- optional | Will color the edges
            "label": string     -- optional | Will display a label on the edges 
        }, ...
    ],
    "groups":[
        {
            "id":int,           -- mandatory | Used to map node.group to groups.label
            "label": string     -- mandatory | Used to make a reference in options.json
        }, ...
    ]
}
```
This file is to be put in the dist repository. The web browser will interect with the server to get data.json through a GET request.

Here is an example of this data.json :
```
{
    "nodes": [
        {
            "id": 0,
            "label": "2000",
            "level": 0,
            "group": 0
        },
        {
            "id": 1,
            "label": "2001",
            "level": 1,
            "group": 1
        },
        {
            "id": 2,
            "label": "2002",
            "level": 2,
            "group": 0
        }
    ],
    "edges": [
        {
            "from": 0,
            "to": 1
        },
        {
            "from": 1,
            "to": 2
        }
    ],
    "groups":[
        {
            "id":0,
            "label": "group0"
        },
        {
            "id":1,
            "label": "group1"
        },
    ]
}
```

#### options.json :
Next, is to give an options.json to customise the graphs, its color, its structure...
The options.json has many possibilities. It's directly coming from [vis.js-network](https://almende.github.io/vis/docs/network/).
So, you can fill the options.json with the same options as for vis.js-network.
The json should be that way :
```
{
    "options":      -- mandatory | A list of options. Each options will create a different view on the web brwoser.
    [
        {
            "mode": string, -- optional | Has to be unique. It will create a button for each mode/view to browse through.
            "visNetwork":   -- mandatory | options for vis.js-network
            {
                Here you will put the options has used in vis.js-network
            }       
        }, ...
    ]
}
```

This file is to be put in the dist repository. The web browser will interect with the server to get options.json through a GET request.

Here as an example :
```
{
    "options":
    [
        {
            "visNetwork":
            {
                "edges": 
                        {
                            "smooth": 
                            {
                                "type": "cubicBezier"
                            },
                            "arrows": { "to": true },
                            "font":{ "align": "middle"},
                            "length":170
                        },
                "groups":
                        {
                            "useDefaultGroups": true,
                            "group0":{
                                "color": "white",
                                "hidden": "true"
                            },
                            "group1":{
                                "color": "green"
                            },
                        },
                "physics":
                        {
                            "enabled": true

                        }
            }
            
        },
        {
            "mode":"hierarchy",
            "visNetwork":{
                "edges": 
                {
                    "smooth": 
                    {
                    "type": "cubicBezier"
                    },
                    "arrows": { "to": true },
                    "font":{ "align": "middle"},
                    "length":170
                },
                "groups":
                {
                    "useDefaultGroups": true,
                    "group0":{
                        "color":"white",
                        "hidden": false
                    },
                    "group1":{
                        "color": "green"
                    },
                },
                "layout": 
                {
                    "hierarchical": 
                    {
                        "direction": "LR",
                        "sortMethod": "directed",
                        "treeSpacing": 50
                    }
                },
                "interaction": { "dragNodes": false },
                "physics": 
                {
                "enabled": false
                }
            }
        }
    ]
}
```

After having update data.json and options.json the way you want. You can try the them in the web browser.
