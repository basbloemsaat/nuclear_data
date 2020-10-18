import nubase2016 from "../data/nubase2016";
import { DiagramBase } from "./diagram";
import * as d3 from "d3";

let data: Array<Object> = nubase2016.full;

class ZNDiagram extends DiagramBase {
  _zoomlevel: number;
  _center_x: number;
  _center_y: number;
  _offset_x: number;
  _offset_y: number;
  _x: d3.ScaleBand<any>;
  _y: d3.ScaleBand<any>;

  constructor(svg: d3.Selection<SVGElement, {}, HTMLElement, any>) {
    super(svg);

    this._init_chart();
    this._init_event_handlers();
    this._init_boxes();
  }

  _init_chart(): void {
    super._init_chart();
    this._zoomlevel = 1;
    this._g_color_legend = this._svg.append("g").classed("colorlegend", true);

    let rf = function (element: string): Array<string> {
      return Object.keys(
        data.reduce((a: any, v: any) => {
          a[v[element]] = true;
          return a;
        }, {})
      ).sort((a: any, b: any) => {
        return a - b;
      });
    };

    let z_s = rf("Z");
    let n_s = rf("N");

    this._x = d3.scaleBand(z_s, [0, 500]);
    this._y = d3.scaleBand(n_s, [500, 0]);

    this._resize_chart();
  }

  _resize_chart(): void {
    super._resize_chart();

    this._center_x = Math.floor(this._width / 2);
    this._center_y = Math.floor(this._height / 2);

    this._update_color_legend();
    this._update_boxes();
  }

  // draw the axes
  _draw_axes(width: number, height: number): void {
    this._x.range([0, width]);
    this._y.range([height, 0]);

    let x_ticks = this._x.domain().filter(function (d, i) {
      return !(i % 10);
    });
    let y_ticks = this._y.domain().filter(function (d, i) {
      return !(i % 10);
    });

    let left_axis = d3.axisLeft(this._y).tickSizeOuter(0).tickValues(y_ticks);
    this._g_left_axis.call(left_axis);
    let right_axis = d3.axisRight(this._y).tickSizeOuter(0).tickValues(y_ticks);
    this._g_right_axis.call(right_axis);

    let top_axis = d3.axisTop(this._x).tickSizeOuter(0).tickValues(x_ticks);
    this._g_top_axis.call(top_axis);
    let bottom_axis = d3
      .axisBottom(this._x)
      .tickSizeOuter(0)
      .tickValues(x_ticks);
    this._g_bottom_axis.call(bottom_axis);
  }

  _init_event_handlers(): void {
    const me = this;
    this._g_canvas.on(
      "wheel",
      function (e: WheelEvent) {
        e.preventDefault();

        if (e.deltaY < 0) {
          me._zoom_in(e);
        } else if (e.deltaY > 0) {
          me._zoom_out(e);
        }
      },
      { passive: false }
    );

    d3.select(window).on("resize", function (e) {
      me._resize_chart();
    });
  }

  _zoom_in(e: Event): void {
    this._zoomlevel++;
    console.log("zoom in", e);
  }

  _zoom_out(e: Event): void {
    this._zoomlevel = Math.max(1, this._zoomlevel - 1);
    // console.log("zoom out");
  }

  _init_boxes(): void {
    let g = this._g_canvas;

    const boxes = g.selectAll("g.boxcontainer").data(data);

    // add the boxes
    let newboxes = boxes.enter().append("g").classed("boxcontainer", true);
    newboxes.append("rect").classed("box", true);

    this._update_boxes();
  }

  _update_boxes(): void {
    let boxes = this._g_canvas.selectAll("g.boxcontainer");
    boxes.attr("transform", (d: any) => {
      let x = this._x(d["Z"]);
      let y = this._y(d["N"]);
      return `translate(${x},${y})`;
    });

    boxes
      .selectAll("rect.box")
      .attr("width", this._x.bandwidth())
      .attr("height", this._y.bandwidth())
      .style("fill", color_box);

    // boxes contents depending on zoom level
  }

  _update_color_legend(): void {
    this._g_color_legend
      .append("rect")
      .attr("x", 100)
      .attr("y", 100)
      .attr("width", 100)
      .attr("height", 100);
  }
}

let hlcr: any; //d3.ScaleLinear<any,any>;
{
  // half life color range

  // get the nubase2016 halflife domain as an array
  let halflife_domain = nubase2016.half_life_domain;

  let hlcr_low = d3.scaleLog(
    [halflife_domain[1], halflife_domain[0]],
    ["white", "red"]
  );
  let hlcr_high = d3.scaleLog(
    [halflife_domain[1], halflife_domain[0]],
    ["blue", "green"]
  );

  // todo, make proper scale. Will do for now
  hlcr = function (v: any) {
    if (v < 2) {
      return hlcr_low(v);
    }
    if (v >= 2) {
      return hlcr_high(v);
    }
    // console.log(v);
    return "red";
  };

  console.log(halflife_domain);
  console.log(hlcr(1));
}

const selected_coloring = "half_life";
const color_box = function (d: any) {
  // for now, only one color scale
  return color_box_half_life(d);
};

const color_box_half_life = function (d: any) {
  if (d.half_life == "stbl") {
    return "#000";
  } else if (d.half_life == "unk") {
    return "#0f0";
  }
  return hlcr(d.half_life);
};

export default ZNDiagram;
