import * as d3 from "d3";

// This is a very roundabout way to get the data in. The reason is that
// I want the nubase2016.txt to be unaltered.

// if the nubase data is loaded: exec the callback with the data. Else
// store the callback in the queue and exec it when the data is loaded
let f_queue: Array<(data: any) => void> = [];
let nubase2016_exec = (callback: (data: any) => void) => {
  if (!loaded) {
    f_queue.push(callback);
  } else {
    callback(nubase_obj);
  }
};

let exec_queue = () => {
  for (let i = 0; i < f_queue.length; i++) {
    f_queue[i](nubase_obj);
  }
};

let loading = false;
let loaded = false;

let nubase2016_src_txt = "";
let nubase_obj: NuBase2016;

d3.text("/data/nubase2016.txt").then(function (text) {
  nubase_obj = new NuBase2016(text);
  exec_queue();
});

interface Isotope {
  A: number; // mass number (z+n)
  Z: number; // atomic number / number of protons
  N: number; // number of neutrons
  half_life_secs: number;
  half_life_unit: string;
}

class NuBase2016 {
  _dataraw: String;
  _datafull: Array<Isotope>;

  constructor(source_txt: string) {
    this._dataraw = source_txt;
  }

  get full(): Array<Isotope> {
    if (!this._datafull) {
      this._parse_raw_txt(this._dataraw);
    }
    return this._datafull;
  }

  // get half_life_domain(): Array<number> {
  //   let hld = this.full.reduce(
  //     (a: any, v: any) => {
  //       if (!isNaN(v["half_life_secs"])) {
  //         a[0] = Math.min(a[0], v["half_life_secs"] || 1);
  //         a[1] = Math.max(a[1], v["half_life_secs"] || 1);
  //       }
  //       return a;
  //     },
  //     [1, 1]
  //   );
  //   return hld;
  // }

  _parse_raw_txt(raw: String) {
    let nubase2016_txt = raw.split(/[\r\n]+/);

    this._datafull = nubase2016_txt
      .filter((e, i) => {
        if (i > 0) {
          return e;
        }
      })
      .map((row) => {
        let A = Number.parseInt(row.substring(0, 3), 10);
        let Z = Number.parseInt(row.substring(4, 7), 10);

        let element = row.substring(11, 17).trim();

        let half_life: any = row.substring(60, 69).trim();
        let half_life_unit: string = row.substring(69, 71).trim();
        let half_life_secs: number; // = half_life;
        let log = false;
        if (half_life != "stbl") {
          half_life = Number.parseFloat(half_life);

          if (half_life_unit == "" || half_life_unit == "n") {
            half_life_secs = null; // unknown
          } else if (half_life_unit == "ys") {
            half_life_secs = half_life * 1e-24;
          } else if (half_life_unit == "zs") {
            half_life_secs = half_life * 1e-21;
          } else if (half_life_unit == "as") {
            half_life_secs = half_life * 1e-18;
          } else if (half_life_unit == "fs") {
            half_life_secs = half_life * 1e-15;
          } else if (half_life_unit == "ps") {
            half_life_secs = half_life * 1e-12;
          } else if (half_life_unit == "ns") {
            half_life_secs = half_life * 1e-9;
          } else if (half_life_unit == "us") {
            half_life_secs = half_life * 1e-6;
          } else if (half_life_unit == "ms") {
            half_life_secs = half_life * 1e-3;
          } else if (half_life_unit == "s") {
            half_life_secs = half_life;
          } else if (half_life_unit == "m") {
            half_life_secs = half_life * 60;
          } else if (half_life_unit == "h") {
            half_life_secs = half_life * 3600;
          } else if (half_life_unit == "d") {
            half_life_secs = half_life * 86400;
          } else if (half_life_unit == "y") {
            half_life_secs = half_life * 31556926;
          } else if (half_life_unit == "ky") {
            half_life_secs = half_life * 31556926 * 1e3;
          } else if (half_life_unit == "My") {
            half_life_secs = half_life * 31556926 * 1e6;
          } else if (half_life_unit == "Gy") {
            half_life_secs = half_life * 31556926 * 1e9;
          } else if (half_life_unit == "Ty") {
            half_life_secs = half_life * 31556926 * 1e12;
          } else if (half_life_unit == "Py") {
            half_life_secs = half_life * 31556926 * 1e15;
          } else if (half_life_unit == "Ey") {
            half_life_secs = half_life * 31556926 * 1e18;
          } else if (half_life_unit == "Yy") {
            half_life_secs = half_life * 31556926 * 1e21;
          } else if (half_life_unit == "Zy") {
            half_life_secs = half_life * 31556926 * 1e24;
          } else {
            log = true;
            console.log(element, half_life_unit);
          }
        }

        let rv = {
          A: A, // mass number
          Z: Z, // atomic number, number of protons
          N: A - Z, // number of neutrons
          level: row.substring(7, 9).trim(), //?
          element: element,
          mass_excess: Number.parseFloat(row.substring(18, 29).trim()), //keV
          mass_excess_s: Number.parseFloat(row.substring(29, 38).trim()),
          exitation_energy: row.substring(38, 48).trim(), //keV
          exitation_energy_s: row.substring(48, 56).trim(),
          exitation_energy_origin: row.substring(56, 60).trim(),
          half_life: half_life,
          half_life_unit: row.substring(69, 71).trim(),
          half_life_s: Number.parseFloat(row.substring(72, 78)),
          half_life_secs: half_life_secs,
          Jpi: row.substring(79, 92).trim(),
          ens: Number.parseInt(row.substring(93, 95)), //year, 2 digits
          reference: row.substring(96, 103).trim(),
          discovery: Number.parseInt(row.substring(104, 109)),
          decay: row.substring(110).trim(),
        };

        if (log) {
          console.log(rv);
        }

        return rv;
      });
  }
}

export { nubase2016_exec, NuBase2016, Isotope };
