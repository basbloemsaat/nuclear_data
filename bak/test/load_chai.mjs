// use as import {expect} from "../load_chai.mjs";

import * as chai_i from "../node_modules/chai/chai.js";
import "../node_modules/chai/chai.js";

let chai_export;

if (typeof window !== "undefined") {
    // in de browser
    chai_export = chai;
} else {
    // in node
    chai_export = chai_i.default;
}

export default chai_export;
const expect = chai_export.expect;
export {expect};
