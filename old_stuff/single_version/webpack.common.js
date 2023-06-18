const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: {
    index: "./source/ts/index.ts",
    chart_of_nuclides: "./source/ts/chart_of_nuclides.ts",
  },
  plugins: [
    new HtmlWebpackPlugin({
      filename: "index.html",
      template: "source/html/index.html",
      chunks: ["index"],
    }),
    new HtmlWebpackPlugin({
      filename: "chart_of_nuclides.html",
      template: "source/html/index.html",
      chunks: ["chart_of_nuclides"],
    }),
  ],
  mode: "production",

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

      {
        test: /\.s[ac]ss$/i,
        use: [
          // Creates `style` nodes from JS strings
          "style-loader",
          // Translates CSS into CommonJS
          "css-loader",
          // Compiles Sass to CSS
          "sass-loader",
        ],
      },

      {
        test: /\.jpg/,
        type: "asset/inline",
      },
    ],
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },
};
