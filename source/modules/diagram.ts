import * as d3 from "d3";

class Diagram {
  _svg: any; // any to be able to add { passive: false } to the wheel event

  _g_canvas: any;
  _g_left_axis: any; // any because node().getBBox();
  _g_right_axis: any; // any because node().getBBox();
  _g_top_axis: any; // any because node().getBBox();
  _g_bottom_axis: any; // any because node().getBBox();
  _g_color_legend: any; // any because node().getBBox();

  _width: number;
  _height: number;
  _canvas_width: number;
  _canvas_height: number;

  constructor(svg: d3.Selection<SVGElement, {}, HTMLElement, any>) {
    this._svg = svg;
  }

  _init_chart(): void {
    this._g_canvas = this._svg.append("g").classed("canvas", true);
    this._g_canvas.append("rect").classed("background", true); // background rect as target for wheel event
    this._g_left_axis = this._svg.append("g").classed("left", true);
    this._g_right_axis = this._svg.append("g").classed("right", true);
    this._g_top_axis = this._svg.append("g").classed("top", true);
    this._g_bottom_axis = this._svg.append("g").classed("bottom", true);
  }

  _resize_chart(): void {
    this._width = this._svg.node().clientWidth;
    this._height = this._svg.node().clientHeight;

    this._svg.attr("viewBox", `0 0 ${this._width} ${this._height}`);

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

  _draw_axes(width: number, height: number): void {}
}

export { Diagram };
