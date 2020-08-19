import "https://d3js.org/d3.v5.js";

Promise.all([
    d3.text("/data/Nubase2016/nubase2016.txt")
]).then(function ([nubase2016_txt]) {
    nubase2016_txt = nubase2016_txt.split(/[\r\n]+/);
    let nubase2016 = nubase2016_txt.map(row => {
        return {
            A: Number.parseInt(row.substr(0, 3), 10), // mass number
            Z: Number.parseInt(row.substr(4, 3), 10), // atomic number
            level: row.substr(7, 3), //
            element: row.substr(11, 6),
            mass_excess: row.substr(18, 11),
            mass_excess_unc: row.substr(29, 9),

        };
    });

    let checkrow = rownr => {
        console.log(`${rownr}; ${nubase2016_txt[rownr - 1]}`);
        console.log(JSON.stringify(nubase2016[rownr - 1]));
    };

    checkrow(1);
    checkrow(2);
    checkrow(418);
    checkrow(1737);

});