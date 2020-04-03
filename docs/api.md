# UrbanCo2Fab REST API
UrbanCo2Fab API runs on the following port and the first version can be accessed in the following manner

* port: 8890
* API: /urbanco2fab/v1.0/ 

## Running UrbanCo2Fab API
Following are the commands to run urbanco2fab API
<pre> 
$ cd urbanco2fab
$ ./urbanco2fab run
</pre> 

On a test environment, you will get the following information
<pre> 
 * Running on http://127.0.0.1:8890/ (Press CTRL+C to quit)
</pre> 

Check the above link on the browser with any of the operations given below

## operations
* **API Operation** : '/urbanco2fab/v1.0/'
* **Goal** : gives a list of all resources exposed by urbanco2fab API
### Response
<pre>
- operations
  * operation:
     * methods: GET, OPTIONS,...
     * resource:
</pre>

## workspace
* **API Operation** : '/urbanco2fab/v1.0/workspace'
* **Goal**: responds with all the information required to visualize a workspace.
### response
<pre>
- node
	* id (mandatory)
    * title (mandatory): Currently has following information
            * date (mandatory)
	* label (mandatory)
	* level (mandatory for hierarchie)
	* group_id (optional)
- edge
	* from "id_node" (mandatory)
	* to "id_node" (mandatory)
	* color (optional)
	* label (optional)
- group
	* id (mandatory)
	* color (optional)
	* mode (optional)
	* label (optional) 
</pre>

**Note**

* title (mandatory): Information that will be shown on overlay (Viznetwork documentation)
* label (mandatory): Information that will be shown inside the node (Viznetwork documentation)

