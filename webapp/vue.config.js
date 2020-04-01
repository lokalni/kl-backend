const webpack = require('webpack');

module.exports = {
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
          'process.env.BACKEND_URL': JSON.stringify(process.env.BACKEND_URL),
      }),
    ]
  }
};

