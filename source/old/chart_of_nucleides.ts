import "./site";
import { Diagram } from "./modules/diagram";
import * as d3 from "d3";
import { nubase2016_exec, NuBase2016 } from "./modules/nubase2016";

const diag = new Diagram(d3.select("svg#zndiagram"));

let init_function = (data: NuBase2016) => {
  console.log(data.full);
};

nubase2016_exec(init_function);
