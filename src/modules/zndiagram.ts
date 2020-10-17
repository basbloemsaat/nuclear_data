import nubase2016 from "./nubase2016";
import * as d3 from "d3";
import { BaseType } from "d3";

let data: Array<Object> = nubase2016.full;

class ZNDiagram {
  _svg: any; // any to be able to add { passive: false } to the wheel event
  _g: d3.Selection<SVGElement, {}, HTMLElement, any>;
  _zoomlevel: number;
  _width: number;
  _height: number;
  _center_x: number;
  _center_y: number;

  constructor(svg: d3.Selection<SVGElement, {}, HTMLElement, any>) {
    this._svg = svg;

    this._init_chart();
    this._init_zoom();
    this._init_boxes();
  }

  _init_chart(): void {
    this._zoomlevel = 0;

    // width and heigth
    this._width = this._svg.node().clientWidth;
    this._height = this._svg.node().clientHeight;

    this._center_x = Math.floor(this._width / 2);
    this._center_y = Math.floor(this._height / 2);

    this._zoom_viewBox();

    // let x = reduce_function

    let z_s = Object.keys(
      data.reduce((a: any, v: any) => {
        a[v.Z] = true;
        return a;
      }, {})
    ).sort((a: any, b: any) => {
      return a - b;
    });

    let n_s = Object.keys(
      data.reduce((a: any, v: any) => {
        a[v.A - v.Z] = true;
        return a;
      }, {})
    ).sort((a: any, b: any) => {
      return a - b;
    });

    console.log(n_s);
  }

  _zoom_viewBox(): void {
    // TODO: zoom
    this._svg.attr("viewBox", `0 0 ${this._width} ${this._height}`);
  }

  _init_zoom(): void {
    const me = this;
    this._svg.on(
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
    // console.log("zoom in");
  }

  _zoom_out(e: Event): void {
    // console.log("zoom out");
  }

  _init_boxes(): void {
    this._g = this._svg.append("g").classed("boxes", true);
    let g = this._g;

    const boxes = g.selectAll("g.boxcontainer").data(data);

    // add the boxes
    boxes.enter().append("g").classed("box", true);
    this._update_boxes(boxes.merge(boxes.enter()));
  }

  _update_boxes(boxes?: d3.Selection<BaseType, {}, SVGElement, any>): void {
    if (boxes === undefined) {
      boxes = this._g.selectAll("g.boxcontainer");
    }

    // boxes are filled depending on zoom level
  }
}

export default ZNDiagram;
