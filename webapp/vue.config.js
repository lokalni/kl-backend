const webpack = require('webpack');

module.exports = {
  devServer: {
    proxy: {
      "/": {
        target: "http://kl-backend:8000",
      },
    },
    // proxy: 'http://localhost:8000'
    // proxy: 'http://kl-backend:8000',
  },
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
          'process.env.BACKEND_URL': JSON.stringify(process.env.BACKEND_URL),
      }),
    ]
  },
}

