const path = require('path');

module.exports = {
  entry: './src/viz.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist'),
  },
};