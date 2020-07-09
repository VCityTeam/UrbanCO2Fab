const express = require('express'); // import express
const app = express(); // initialise the server
const port = 3000; // Choose the listening port of your application

app.get('/', (req, res) => res.send('Hello World!')); // Add a route for url "localhost:3000/" that will answer "Hello world" to a GET request

app.use(express.static(__dirname + '/public')); // Serves resources from public folder

var server = app.listen(port, function(){
    var host = server.address().address
    var port = server.address().port
    
    console.log("App listening at http://%s:%s", host, port)}); // Make your app listening to your chosen port