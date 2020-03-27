# UrbanCo2Fab API

## workspace
### JSON response

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

#### title vs label (for node only)
* title (mandatory): Information that will be shown on overlay (Viznetwork documentation)
* label (mandatory): Information that will be shown inside the node (Viznetwork documentation)


