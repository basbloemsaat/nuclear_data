import "./site";
import { Diagram } from "./modules/diagram";
import * as d3 from "d3";

const diag = new Diagram(d3.select("svg#zndiagram"));
