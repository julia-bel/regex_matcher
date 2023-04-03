#!/usr/bin/env node

var fs = require('fs');

var result = new Object();
result.input = process.argv[2];
result.regex = process.argv[3];
result.language = "javascript";
result.valid = false;
result.length = result.input.length;
result.matched = false;
result.time = 0;

try {
    var re = new RegExp("^" + result.regex + "$");
    result.valid = true;
    var start = new Date().getTime() / 1000;
    var matched = result.input.match(re);
    var final = new Date().getTime() / 1000;
    result.matched = Boolean(matched);
    result.time = final - start;
} catch (e) {
    result.valid = false;
}

console.log(JSON.stringify(result));
process.exit(0);
