module.exports = {
  mode: "development",
  entry: {
    index: "./src/index.ts",
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
      // {
      //   test: /\.css$/i,
      //   use: ["style-loader", "css-loader"],
      //   exclude: [/node_modules/, "./fe_old/"],
      // },
    ],
  },
};
