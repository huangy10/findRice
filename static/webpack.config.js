// webpack.config.js
module.exports = {
  entry: {
    list: './modules/list/js/list.js',
    detail: './modules/detail/js/detail.js',
    mine: './modules/mine/js/mine.js',
    login: './modules/login/js/login.js',
    register: './modules/register/js/register.js',
    'create-basic': './modules/createaction/js/create-basic.js',
    'create-criteria': './modules/createaction/js/create-criteria.js',
    create: './modules/createaction/js/create.js'
  },
  output: {
    path: 'build',
    filename: '[name].js'       
  },
  module: {
    loaders: [
      { test: /\.less$/, loader: 'style-loader!css-loader!less-loader' },
      { test: /\.css$/, loader: 'style-loader!css-loader' }
    ]
  },
  resolve: {
    // 现在可以写 require('file') 代替 require('file.less')
    extensions: ['', '.js', '.css', '.less'] 
  }
};