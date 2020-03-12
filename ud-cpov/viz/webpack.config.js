const path = require('path');

module.exports = {
  entry: './src/viz.js',
  target: 'node',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  }

};