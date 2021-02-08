// interface Isotope {
//   A: number; // mass number (z+n)
//   Z: number; // atomic number / number of protons
//   N: number; // number of neutrons
//   half_life_secs: number;
//   half_life_unit: string;
// }

class Isotope {
  private _A: number; // mass number (z+n)
  private _Z: number; // atomic number / number of protons
  private _N: number; // number of neutrons
  private _half_life_secs: number;
  private _half_life_raw: any;
  private _half_life: number | "stable";
  half_life_unit: string;
  half_life_s: number;

  constructor(Z: number, N: number) {
    this._Z = Z;
    this._N = N;
    this._A = Z + N;
  }

  set half_life(val: any) {
    this._half_life_raw = val;

    switch (val) {
      case undefined:
      case null:
      case "":
        this._half_life = null;
        break;
      case "stbl":
        this._half_life = "stable";
        break;
      default:
        if (typeof val == "string") {
          switch (val.substr(0, 1)) {
            // because in this case the ballpark is better than nothing:
            case "~":
            case ">":
            case "<":
              val = val.substr(1);
          }
          switch (val.substr(0, 2)) {
            // because in this case the ballpark is better than nothing:
            case "R=":
            case "R<":
              val = val.substr(2);
          }
          if (Number.parseFloat(val) > 0) {
            this._half_life = Number.parseFloat(val);
          } else {
            this._half_life = null;
            // console.log(val)
          }
        }
    }
  }

  get half_life_secs(): number {
    if (this._half_life_secs === undefined) {
      
      this._half_life_secs = 0;
    }
    return this._half_life_secs;
  }
}

export { Isotope };
