'use strict';

if (process.argv.length < 3) {
    console.log(`usage: node ${__filename} taskName`);
    process.exit(1);
}
const taskName = process.argv[2]
console.log(`taskName: ${taskName}`)