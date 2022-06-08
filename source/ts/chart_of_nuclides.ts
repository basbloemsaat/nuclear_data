import * as d3 from "d3";
import "../css/main.scss";

import nubase2016 from "./modules/nubase2016";
import { Isotope } from "./modules/isotope";

const config = {
  margin: 2,
  large_margin: 10,
};

const svg = d3.select("main").append("svg");

let width = svg.node().clientWidth;
let height = svg.node().clientHeight;

const x = d3
  .scaleBand()
  .domain(Array.from(Array(300).keys()).map((e) => `${e}`))
  .range([0, width])
  .paddingInner(0.2);
const y = d3
  .scaleBand()
  .domain(
    Array.from(Array(122).keys())
      .reverse()
      .map((e) => `${e}`)
  )
  .range([0, height])
  .paddingInner(0.2);

const x_axis_g = svg.append("g").classed("x_axis", true);
const y_axis_g = svg.append("g").classed("y_axis", true);
const canvas_g = svg.append("g").classed("canvas", true);

const x_axis = d3.axisBottom(x).tickValues(
  x.domain().filter(function (d, i) {
    return !(i % 10);
  })
);
const y_axis = d3.axisLeft(y).tickValues(
  y.domain().filter(function (d, i) {
    return !(i % 10);
  })
);

// render for measurement
x_axis_g.call(x_axis);
y_axis_g.call(y_axis);

let xheight = x_axis_g.node().getBBox().height;
let ywidth = y_axis_g.node().getBBox().width;

y_axis_g.attr(
  "transform",
  `translate(${config.margin + ywidth},${config.large_margin})`
);
y.range([0, height - config.margin - config.large_margin - xheight]);
y_axis_g.call(y_axis);

x_axis_g.attr(
  "transform",
  `translate(${config.margin + ywidth},${height - config.margin - xheight})`
);

x.range([0, width - config.margin - config.large_margin - ywidth]);
x_axis_g.call(x_axis);

canvas_g.attr(
  "transform",
  `translate(${config.margin + ywidth},${config.large_margin})`
);

nubase2016((data: any) => {
  let m = d3.group(data, (d: Isotope) => d.Z);

  let colorcount = 9;
  let mmm = Array(colorcount)
    .fill("")
    .map((d, i) => d3.interpolateRdYlBu(i / colorcount));
  const hlcolor = d3
    .scaleQuantile()
    .domain(data.map((d: Isotope) => d.half_life))

    //@ts-expect-error
    .range(mmm);
    // .range(d3.schemeRdYlBu[9]); // a bit less pronounced
  canvas_g
    .selectAll("g.row")
    .data(m)
    .join("g")
    .classed("row", true)
    .selectAll("rect.cell")
    .data((d) => {
      return d[1];
    })
    .join("rect")
    .classed("cell", true)
    .classed("stable", (d) => d.stable)
    .attr("x", (d) => x(`${d.A}`))
    .attr("y", (d) => y(`${d.Z}`))
    .attr("width", x.bandwidth())
    .attr("height", y.bandwidth())
    .style("fill", (d) => {
      if (d.stable) {
        return;
      }
      return hlcolor(d.half_life);
    })
    .on("mouseover", (d, e) => {
      console.log(e);
    });
});

console.log(Array.from(Array(5).keys()).map((e) => `${e}`));
