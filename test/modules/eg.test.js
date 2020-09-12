import {Eg} from '../../docs/modules/eg.js';
import {expect} from "../load_chai.mjs";

describe('test eg', function() {

    it('Eg shoud be a class', function () {
        let eg = new Eg();
        expect(eg).to.be.an('Object');
        expect(eg).to.have.property('value').that.equals(1);
    });
});
