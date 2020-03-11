var express = require('express');
var app = express();

//setting middleware
app.use(express.static(__dirname + '/dist')); //Serves resources from public folder


var server = app.listen(5000, function(){
    var host = server.address().address
    var port = server.address().port
    
    console.log("App listening at http://%s:%s", host, port)
});