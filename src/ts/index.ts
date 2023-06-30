import * as d3 from "d3";
import "../css/main.scss";

let ul = d3.select("main").append("ul");

ul.append("li")
  .append("a")
  .attr("href", "chart_of_nuclides.html")
  .text("Chart of nuclides");
