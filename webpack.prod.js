const HtmlInlineScriptPlugin = require("html-inline-script-webpack-plugin");
const { merge } = require("webpack-merge");
const common = require("./webpack.common.js");

module.exports = merge(common, {
  mode: "production",
  plugins: [
    new HtmlInlineScriptPlugin({
      scriptMatchPattern: [/bundle[.]js$/, /app~.+[.]js$/],
    }),
  ],
  output: {
    path: `${__dirname}/dist`,
    filename: "[name].js",
    publicPath: "",
  },
});
