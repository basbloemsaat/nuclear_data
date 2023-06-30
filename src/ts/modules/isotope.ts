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

// helper to separate input
interface IsotopeProperties {
  element?: string;
  half_life?: number;
  half_life_raw?: string;
  stable?: boolean;

  raw?: string;
}

class Isotope {
  public readonly element_name: string;

  public readonly Z: number; // atomic number, # protons
  public readonly A: number; // mass number protons+neutrons
  public readonly N: number; // neutron number, # neutrons

  public readonly half_life: number; // hl in seconds
  public readonly half_life_raw: string; // hl source string
  public readonly stable: boolean; // hl source string

  public readonly raw: string; // nubase2016 row, for debugging mostly

  constructor(Z: number, A: number, properties?: IsotopeProperties) {
    this.element_name = properties.element;
    this.Z = Z;
    this.A = A;
    this.N = Z - A;

    // console.log(properties);
    this.half_life = properties.half_life;
    this.half_life_raw = properties.half_life_raw;
    this.stable = properties.stable;

    this.raw = properties.raw;
  }
}

export { IsotopeProperties, Isotope, half_life_units_factors };
