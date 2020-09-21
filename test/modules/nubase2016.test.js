import nubase2016 from "../../docs/modules/nubase2016.mjs";
import { expect } from "../load_chai.mjs";

describe("nubase 2016", function () {
  it("nubase2016 shoud be a Promise", function () {
    
    expect(nubase2016).to.be.a("Promise");
    // expect(eg).to.have.property("value").that.equals(1);
  });
});
