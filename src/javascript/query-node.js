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
    var start = process.hrtime();
    var matched = result.input.match(re);
    var final = process.hrtime();
    result.matched = Boolean(matched);
    result.time = (final[0] - start[0]) + (final[1] - start[1]) / 10**9;
} catch (e) {
    result.valid = false;
}

console.log(JSON.stringify(result));
process.exit(0);
