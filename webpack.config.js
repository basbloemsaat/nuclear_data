module.exports = {
  mode: "development",
  entry: {
    index: "./source/index.ts",
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: [/node_modules/,/pre_docker/]
      },
      
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
        exclude: [/node_modules/,/pre_docker/]
      },
      {
        test: /\.s[ac]ss$/i,
        use: ["style-loader", "css-loader", "sass-loader"],
        exclude: [/node_modules/,/pre_docker/]
      },
    ],
  },
};
