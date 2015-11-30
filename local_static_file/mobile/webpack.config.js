// webpack.config.js
var webpack = require('webpack');
var isProd = JSON.parse(process.env.PROD || "0");

module.exports = {
  entry: {
    list:               './modules/list/js/list.js',
    detail:             './modules/detail/js/detail.js',
    'create':           './modules/createaction/js/create.js',
    'create-basic':     './modules/createaction/js/create-basic.js',

    'create-criteria':  './modules/createaction/js/create-criteria.js',
    'message':     './modules/message/js/message.js',
    'mine':     './modules/mine/js/mine.js',
    'activity':     './modules/activity/js/activity.js',
    'register':     './modules/register/js/register.js',
    'login':     './modules/login/js/login.js',
    'search':     './modules/search/js/search.js',

  },
  devtool: isProd ? '' : 'source-map',
  output: {
    path: 'build',
    filename: '[name].js'       
  },
  module: {
    loaders: [
      { test: /\.less$/, loader: isProd ? 'style!css!less' : 'style!css?sourceMap!less' },
      { test: /\.css$/, loader: isProd ? 'style!css' : 'style!css?sourceMap'}
    ]
  },
  resolve: {
    // 现在可以写 require('file') 代替 require('file.less')
    extensions: ['', '.js', '.css', '.less'] 
  },
  plugins: isProd ? [
    new webpack.optimize.UglifyJsPlugin({minimize: true})
  ] : []
};