//var errors = require('./errors');

function API_Items_Collection() {
  this.store = {};
  this.lastId = 0;
}

API_Items_Collection.prototype.seed = function(obj, cb) {
this.store = obj;
cb();
};

API_Items_Collection.prototype.findAll = function(cb) {
var items = [];

for (var id in this.store) {
    items.push(this.store[id]);
}

cb(null, items);
};

API_Items_Collection.prototype.create = function(obj, cb) {
this.lastId++;
obj.id = this.lastId;
this.store[this.lastId] = obj;
cb(null, obj);
};

API_Items_Collection.prototype.update = function(id, obj, cb) {
this.find(id, function(err, item) {
    if (err) return cb(err);
    item = obj;
    cb(null, item);
});
};

API_Items_Collection.prototype.patch = function(id, obj, cb) {
this.find(id, function(err, item) {
    if (err) return cb(err);

    for (var key in obj) {
    item[key] = obj[key];
    }

    cb(null, item);
});
};

API_Items_Collection.prototype.find = function(id, cb) {
id = parseInt(id, 10);
var obj = this.store[id];
if (obj) {
    cb(null, obj);
} else {
    cb(new errors.NotFound('Item not found'));
}
};

API_Items_Collection.prototype.remove = function(id, cb) {
id = parseInt(id, 10);
if (this.store[id]) {
    delete this.store[id];
    cb();
} else {
    cb(new errors.NotFound('Item not found'));
}
};

module.exports.pages = new API_Items_Collection('pages');
