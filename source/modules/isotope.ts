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
  half_life: any;
  half_life_unit: string;
  half_life_s: number;

  constructor(Z: number, N: number) {
    this._Z = Z;
    this._N = N;
    this._A = Z + N;
  }

  




}

export { Isotope };
