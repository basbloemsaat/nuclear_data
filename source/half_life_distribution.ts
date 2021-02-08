import "./site";
import { Diagram } from "./modules/diagram";
import * as d3 from "d3";
import { nubase2016_exec, NuBase2016 } from "./modules/nubase2016";
import {Isotope} from "./modules/isotope";

const diag = new Diagram(d3.select("svg#chart_halflifes"));

let init_function = (data: NuBase2016) => {
  let full = data.full;


  return;
  let min_hl = 1;
  let max_hl = 1;

  let hl_unitcount = full.reduce((a: { [key: string]: number }, e: Isotope) => {
    if (e.half_life_secs < min_hl && e.half_life_secs != null) {
      min_hl = e.half_life_secs;
    }
    if (e.half_life_secs > max_hl) {
      max_hl = e.half_life_secs;
    }

    if (!a[e["half_life_unit"]]) {
      a[e["half_life_unit"]] = 0;
    }
    a[e["half_life_unit"]]++;
    return a;
  }, {});
  console.log(hl_unitcount);

  // @ts-expect-error
  let bin = d3.bin().value((d: Isotope) => d.half_life_secs);
  // @ts-expect-erro r
  // console.log(bin(full));

  let svg = d3.select("svg#chart_halflifes");

  //@ts-expect-error
  let svg_width = svg.node().clientWidth;

  let scale_pos = d3.scaleLog().domain([min_hl, max_hl]).range([0, svg_width]);
  // let scale_color = d3.scaleLog().domain([min_hl, max_hl]).range();

  let scale_map_color = d3.scaleLog().domain([min_hl, max_hl]).range([0, 100]);
  var scale_color = d3.scaleSequential(d3.interpolateRdYlBu).domain([0, 100]);

  let g_axis = svg.append("g").attr("transform", "translate(0,20)");
  let axis = d3.axisTop(scale_pos);

  g_axis.call(axis);

  let g_data = svg.append("g").attr("transform", "translate(0,50)");

  let cs = g_data.selectAll("circle.n").data(full);

  let newcs = cs
    .enter()
    .append("circle")
    .attr("class", "datapoint")
    .attr("r", 2)
    .attr("cx", (d) => {
      if (d.half_life_secs <= 0) {
        return 0;
      }
      return scale_pos(d.half_life_secs);
    })
    .attr("fill", (d) => {
      return scale_color(scale_map_color(d.half_life_secs));
    });
};

nubase2016_exec(init_function);
