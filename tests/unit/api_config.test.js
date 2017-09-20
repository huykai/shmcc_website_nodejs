'use strict';

let chai = require('chai');
let expect = chai.expect;
let should = chai.should();
let sinon = require('sinon');
const api_config = require('../../src/config/api_config.js');

describe('Test api_config.js', function(){

    before(function(){

    });
    after(function(){

    });
    beforeEach(function(){

    });
    afterEach(function(){

    });

    it('api_config at least have five items', function(){
        expect(api_config.length).to.be.above(4);
    });
});
