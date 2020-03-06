var express = require('express');
var app = express();

app.use(express.static(__dirname + '/static/', {
    index: false, 
    immutable: true, 
    cacheControl: true,
    maxAge: "30d"
})); // declare static folder

app.get('/', function (req, res) {
    res.sendFile(__dirname + "/static/" + "graph.html"); //serve file
 })
 
 var server = app.listen(8081, function () {
    var host = server.address().address
    var port = server.address().port
 
    console.log("Example app listening at http://%s:%s", host, port)
 })
