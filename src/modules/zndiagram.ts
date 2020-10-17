import nubase2016 from "./nubase2016";
import * as d3 from "d3";
import { BaseType } from "d3";

let data: Array<Object> = nubase2016.full;

class ZNDiagram {
  _svg: any; // any to be able to add { passive: false } to the wheel event
  _g_canvas: any;
  _g_left_axis: any; // any because node().getBBox();
  _g_right_axis: any; // any because node().getBBox();
  _g_top_axis: any; // any because node().getBBox();
  _g_bottom_axis: any; // any because node().getBBox();
  _zoomlevel: number;
  _width: number;
  _height: number;
  _canvas_width: number;
  _canvas_height: number;
  _center_x: number;
  _center_y: number;
  _offset_x: number;
  _offset_y: number;
  _x: d3.ScaleBand<any>;
  _y: d3.ScaleBand<any>;

  constructor(svg: d3.Selection<SVGElement, {}, HTMLElement, any>) {
    this._svg = svg;

    this._init_chart();
    this._init_zoom();
    this._init_boxes();
  }

  _init_chart(): void {
    this._zoomlevel = 1;

    this._g_canvas = this._svg.append("g").classed("canvas", true);
    this._g_canvas.append("rect").classed("background", true); // background rect as target for wheel event
    this._g_left_axis = this._svg.append("g").classed("left", true);
    this._g_right_axis = this._svg.append("g").classed("right", true);
    this._g_top_axis = this._svg.append("g").classed("top", true);
    this._g_bottom_axis = this._svg.append("g").classed("bottom", true);

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
    this._width = this._svg.node().clientWidth;
    this._height = this._svg.node().clientHeight;
    this._svg.attr("viewBox", `0 0 ${this._width} ${this._height}`);

    this._center_x = Math.floor(this._width / 2);
    this._center_y = Math.floor(this._height / 2);

    this._draw_axes(this._width, this._height); // first time drawing axes full height and width are used. First draw is used for measurements;

    let left_axis_width = Math.ceil(
      this._g_left_axis.node().getBBox()["width"]
    );
    let right_axis_width = Math.ceil(
      this._g_right_axis.node().getBBox()["width"]
    );

    let top_axis_height = Math.ceil(
      this._g_top_axis.node().getBBox()["height"]
    );
    let bottom_axis_height = Math.ceil(
      this._g_bottom_axis.node().getBBox()["height"]
    );

    this._canvas_width = this._width - left_axis_width - right_axis_width;
    this._canvas_height = this._height - top_axis_height - bottom_axis_height;

    this._g_canvas.attr(
      "transform",
      `translate(${left_axis_width},${top_axis_height})`
    );

    d3.select("rect.background")
      .attr("width", this._canvas_width)
      .attr("height", this._canvas_height);

    this._g_left_axis.attr(
      "transform",
      `translate(${left_axis_width},${top_axis_height})`
    );

    this._g_right_axis.attr(
      "transform",
      `translate(${left_axis_width + this._canvas_width},${top_axis_height})`
    );

    this._g_top_axis.attr(
      "transform",
      `translate(${left_axis_width},${top_axis_height})`
    );

    this._g_bottom_axis.attr(
      "transform",
      `translate(${left_axis_width},${top_axis_height + this._canvas_height})`
    );

    this._draw_axes(this._canvas_width, this._canvas_height); // first time drawing axes actual canvas dimensions are used.
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

  _init_zoom(): void {
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
      .style("fill", (d: any) => {
        // console.log(d);
        if(d.half_life == "stbl") {
          return '#000'
        }
        return "#aaa";
      });
    // .attr('transform', d => {
    //   console.log(d);
    //   return 'translate(0,0)'
    // })

    // boxes are filled depending on zoom level
  }
}

export default ZNDiagram;
