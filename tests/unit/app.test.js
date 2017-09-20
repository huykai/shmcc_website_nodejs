var app = require('../../src/app.js');
var expect = require('chai').expect;
var sinon = require('sinon');

describe('app.js test',function(){
    beforeEach(function(done){
        done();
    });
    it('app config test', function() {
        expect(app.get('port')).to.be.equal(3000);
    })
})