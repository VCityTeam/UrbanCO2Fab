var webpack = require('webpack');
var path = require('path');
var fs = require('fs');

module.exports = {
  entry: './src/viz.js',
  target: 'node',
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'main.js'
  },
}