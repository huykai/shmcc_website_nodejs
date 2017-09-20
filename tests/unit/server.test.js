var server = require('../../src/server.js');
var expect = require('chai').expect;

describe('server.js test',function(){
    it('server config', function() {
        expect(server.host).to.be.equal('127.0.0.1');
        expect(server.port).to.be.equal(3000);
    })
})