var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  // devtool: 'source-map',
   entry: [
     './src/index'
   ],
  output: {
    path: path.join(__dirname, './static'),
    filename: 'bundle.js'
  },
  plugins: [
    new ExtractTextPlugin('style.css', {
      allChunks: true
    })
  ],
  module: {
    loaders: [
      // SASS
      {
        test: /\.scss$/,
        // include: path.join(__dirname, 'src'),
        // loaders: ['style', 'css', 'sass']
        loader: ExtractTextPlugin.extract(
          'style', // backup loader when not building .css file
          'css!sass' // loaders to preprocess CSS
        )
      }
    ]
  }
};
