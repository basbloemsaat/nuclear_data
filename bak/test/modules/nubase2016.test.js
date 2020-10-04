import nubase2016 from "../../docs/modules/nubase2016.mjs";
import { expect } from "../load_chai.mjs";

// console.log(nubase2016);


  it("nubase2016 should be an Object", function () {
    expect(nubase2016).to.be.an("Object");
  });

  it("nubase2016 has the full data", function () {
    expect(nubase2016).has.property("full");
    expect(nubase2016.full).to.be.an('Array').to.have.lengthOf(5625);
  });
});
