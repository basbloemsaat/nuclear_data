var HtmlWebpackPlugin = require("html-webpack-plugin");
var path = require("path");

module.exports = {
  mode: "development",
  entry: {
    index: "./source/index.ts",
    chart_of_nucleides: "./source/chart_of_nucleides.ts",
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: [/node_modules/, /pre_docker/],
      },
      {
        test: /\.s[ac]ss$/i,
        use: ["style-loader", "css-loader", "sass-loader"],
        exclude: [/node_modules/, /pre_docker/],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "source/index.ejs",
      filename: "index.html",
      chunks: ["index"],
    }),
    new HtmlWebpackPlugin({
      template: "source/chart_of_nucleides.ejs",
      filename: "chart_of_nucleides.html",
      chunks: ["chart_of_nucleides"],
    }),
  ],
};
