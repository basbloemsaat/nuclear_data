import nubase2016 from "./nubase2016";
import * as d3 from "d3";
import { BaseType } from "d3";

let data: Array<Object> = nubase2016.full;
console.log(data);

class ZNDiagram {
  _svg:  any; // any to be able to add { passive: false } to the wheel event
  _g: d3.Selection<SVGElement, {}, HTMLElement, any>;
  _zoomlevel: number;

  constructor(svg: d3.Selection<SVGElement, {}, HTMLElement, any>) {
    this._svg = svg;
    this._zoomlevel = 0;

    this._init_zoom();
    this._init_boxes();
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
    console.log("zoom in");
  }

  _zoom_out(e: Event): void {
    console.log("zoom out");
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
