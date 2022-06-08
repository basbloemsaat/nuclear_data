import * as d3 from "d3";
import { IsotopeProperties, Isotope } from "./isotope";

const half_life_units_factors: { [key: string]: number } = {
  ys: 1e-24,
  zs: 1e-21,
  as: 1e-18,
  fs: 1e-15,
  ps: 1e-12,
  ns: 1e-9,
  us: 1e-6,
  ms: 1e-3,
  s: 1,
  m: 60,
  h: 60 * 60,
  d: 24 * 60 * 60,
  y: 31557600,
  ky: 31557600 * 1e3,
  My: 31557600 * 1e6,
  Gy: 31557600 * 1e9,
  Ty: 31557600 * 1e12,
  Py: 31557600 * 1e15,
  Ey: 31557600 * 1e18,
  Yy: 31557600 * 1e21,
  Zy: 31557600 * 1e24,
};

const parse_line = (row: string, i: number): Isotope => {
  let A = Number.parseInt(row.substring(0, 3), 10);
  let Z = Number.parseInt(row.substring(4, 7), 10);
  let properties: IsotopeProperties = {
    raw: row,
  };

  {
    //half life related

    const half_life = row.substring(60, 69).trim();
    const half_life_unit: string = row.substring(69, 71).trim();
    properties.half_life_raw = `${half_life}${half_life_unit}`;

    if (half_life == "stbl") {
      properties.stable = true;
    } else {
      let factor = half_life_units_factors?.[half_life_unit];
      if (factor) {
        properties.half_life = parseFloat(half_life) * factor;
        properties.stable = false;
      } else if (half_life != "") {
        // console.log(i, half_life);
      }
    }
  }

  {
    properties.element_name = row.substring(11, 17).trim();
  }

  const iso = new Isotope(Z, A - Z, properties);
  return iso;
};

const asyncfuncion = async () => {
  let raw = await d3.text("./data/nubase2016.txt");
  let nubase2016_txt = raw.split(/[\r\n]+/);
  let res = nubase2016_txt
    .filter((row) => row != "")
    .filter((row) => {
      // filter out all exited states
      let element = row.substring(11, 17).trim();
      return !element.match(/[a-zA-Z]+|[0-9]+/g)[1][2];
    })
    .map((row, i: number) => {
      return parse_line(row, i);
    });
  return res;
};

export {};

export default (callback: (data: any) => void) => {
  asyncfuncion().then(callback);
};
