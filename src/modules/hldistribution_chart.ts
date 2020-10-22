import nubase2016, { Isotope } from "../data/nubase2016";
import { DiagramBase } from "./diagram";
import * as d3 from "d3";

let data: Array<number> = nubase2016.full.map(function (v: Isotope) {
  return Math.log(v["half_life_secs"]);
});

// })
let half_life_domain = nubase2016.half_life_domain.map((v) => Math.log(v));
// console.log(half_life_domain);

let bin = d3.histogram(); //v5 alias because @types/d3 is stuck at v5

let hdata = bin(
  data.filter(function (v: any) {
    let x = parseFloat(v);
    return x.toString() == v && x != -Infinity;
  })
);

class HLDistribution extends DiagramBase {
  _x: d3.ScaleBand<any>;
  _y: d3.ScaleLinear<any, any>;

  constructor(svg: d3.Selection<SVGElement, {}, HTMLElement, any>) {
    super(svg);

    this._init_chart();
    this._resize_chart();
    this._draw_bars();
    // this._draw_axes();
  }

  _init_chart(): void {
    super._init_chart();
    this._x = d3.scaleBand();
    this._y = d3.scaleLinear().domain([0, 100]);

    //spacers in unused axis. Crude but it works best.
    this._g_right_axis.append("rect").classed("spacer", true);
    this._g_top_axis.append("rect").classed("spacer", true);
  }

  _draw_axes(width: number, height: number): void {
    // console.log(width);
    this._x.range([0, width]);
    this._y.range([height, 0]);

    let left_axis = d3.axisLeft(this._y); // .tickSizeOuter(0);
    this._g_left_axis.call(left_axis);
    let bottom_axis = d3.axisBottom(this._x); //.tickSizeOuter(0);
    //   .tickValues(x_ticks);
    this._g_bottom_axis.call(bottom_axis);
  }

  _draw_bars(): void {
    let bars = this._g_canvas.selectAll("g.bar").data(hdata);

    bars.exit().remove();
    let newbars = bars.enter().append("g").classed("bar", true);
    newbars.append("rect").classed("bar");

    
  }
}

export default HLDistribution;
