import {text} from "https://d3js.org/d3.v5.js";

Promise.all([
    d3.text("/data/Nubase2016/nubase2016.txt")
]).then(function ([nubase2016_txt]) {
    nubase2016_txt = nubase2016_txt.split(/[\r\n]+/);
    let nubase2016 = nubase2016_txt.map(row => {
        let retval = {
            A: Number.parseInt(row.substring(0, 3), 10), // mass number
            Z: Number.parseInt(row.substring(4, 7), 10), // atomic number
            level: row.substring(7, 9).trim(), //
            element: row.substring(11, 17).trim(),
            mass_excess: row.substring(18, 29).trim(), //keV
            mass_excess_s: row.substring(29, 38).trim(),
            exitation_energy: row.substring(38, 48).trim(), //keV
            exitation_energy_s: row.substring(48, 56).trim(),
            exitation_energy_origin: row.substring(56, 60).trim(),
            half_life: row.substring(60, 71),
            half_life_unit: row.substring(69, 71),
            half_life_s: row.substring(72, 78),
            Jpi: row.substring(79, 92),
            ens: row.substring(93, 95), //year, 2 digits
            reference: row.substring(96, 103),
            discovery: row.substring(104, 109),
            decay: row.substring(110),
        };

        return retval;
    });

    let checkrow = rownr => {
        console.log(`${rownr}; ${nubase2016_txt[rownr - 1]}`);
        console.log(JSON.stringify(nubase2016[rownr - 1]));
    };

    checkrow(1);
    // checkrow(2);
    checkrow(1697);
    checkrow(1700);
    // checkrow(286);
    // checkrow(1989);

});