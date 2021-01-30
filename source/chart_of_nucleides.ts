import "./site";
import { Diagram } from "./modules/diagram";
import * as d3 from "d3";
import {nubase2016_exec} from "./modules/nubase2016";


const diag = new Diagram(d3.select("svg#zndiagram"));

let callback = (data:any) => {
    console.log(data);
}

nubase2016_exec(callback);