import nubase2016 from "../data/nubase2016";
import { DiagramBase } from "./diagram";
import * as d3 from "d3";

let data: Array<Object> = nubase2016.full;
let half_life_domain = nubase2016.half_life_domain;
console.log(half_life_domain);

class HLDistribution extends DiagramBase {
    _x: d3.ScaleLinear<any,any>;
    _y: d3.ScaleBand<any>;

    constructor(svg: d3.Selection<SVGElement, {}, HTMLElement, any>) {
        super(svg);
    }

    _draw_axes(width: number, height: number): void {
        this._x.range([0, width]);
        this._y.range([height, 0]);
    }
}

export default HLDistribution;
