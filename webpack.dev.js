const path = require("path");
const { merge } = require("webpack-merge");
const common = require("./webpack.common.js");

module.exports = merge(common, {
  mode: "development",
  devtool: "inline-source-map",
  devServer: {
    static: {
      directory: path.join(__dirname, "docs"),
    },
    compress: false,
    port: 13080,
  },

  output: {
    path: `${__dirname}/docs/`,
    filename: "[name].js",
    publicPath: "",
  },
});
