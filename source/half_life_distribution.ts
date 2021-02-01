import "./site";
import { Diagram } from "./modules/diagram";
import * as d3 from "d3";
import { nubase2016_exec, NuBase2016, Isotope } from "./modules/nubase2016";

const diag = new Diagram(d3.select("svg#chart_halflifes"));

let init_function = (data: NuBase2016) => {
  let full = data.full;

  let hl_unitcount = full.reduce((a: { [key: string]: number }, e: Isotope) => {
    if (!a[e["half_life_unit"]]) {
      a[e["half_life_unit"]] = 0;
    }
    a[e["half_life_unit"]]++;
    return a;
  }, {});
  console.log(hl_unitcount);


};

nubase2016_exec(init_function);
