const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  mode: "development",
  entry: {
    index: "./src/index.ts",
    hldistribution: "./src/hldistribution.ts",
    zndiagram: "./src/zndiagram.ts",
  },
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "docs"),
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "src/index.ejs",
      filename: "index.html",
      chunks: ["index"],
    }),
    new HtmlWebpackPlugin({
      template: "src/hldistribution.ejs",
      filename: "hldistribution.html",
      chunks: ["hldistribution"],
    }),
    new HtmlWebpackPlugin({
      template: "src/zndiagram.ejs",
      filename: "zndiagram.html",
      chunks: ["zndiagram"],
    }),
  ],
};
