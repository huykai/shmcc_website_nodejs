'use strict';

let chai = require('chai');
let expect = chai.expect;
let should = chai.should();
let assert = chai.assert;

const site_config = require('../../src/config/site_config')

describe('Test site_config.js', function(){
    it(' Site_config Config', function(){
        site_config.static_dir.should.be.a('string');
        site_config.home_page.should.be.a('string');
        expect(site_config.home_page).to.be.a('string');
        expect(site_config.static_dir).to.be.a('string');
        assert.typeOf(site_config.static_dir,'string');
        assert.typeOf(site_config.home_page,'string');
    })
});