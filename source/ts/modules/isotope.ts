// helper to seperate input
interface IsotopeProperties {
  element_name?: string;
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

  constructor(Z: number, N: number, properties?: IsotopeProperties) {
    this.element_name = properties.element_name;
    this.Z = Z;
    this.N = N;
    this.A = Z + N;

    // console.log(properties);
    this.half_life = properties.half_life;
    this.half_life_raw = properties.half_life_raw;
    this.stable = properties.stable;

    this.raw = properties.raw;
  }
}

export { IsotopeProperties, Isotope };
