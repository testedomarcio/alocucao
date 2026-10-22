const fs=require('fs'),assert=require('assert/strict');
const html=fs.readFileSync('spot-black-friday/index.html','utf8');
assert(!html.includes('const ended'),'Retired promotion must not overwrite the new fixed prices');
assert(!html.includes('data-normal='),'No legacy expiry prices');
assert(!html.includes('R$ 8,90')&&!html.includes('R$ 16,90'));
assert(html.includes('R$ 12,00')&&html.includes('R$ 30,00'));
assert(html.includes('id="vitrine-vozes"'));
assert(html.includes('id="single-offer-schema"'));
console.log('PASS: Black Friday uses fixed current prices and official showcase, with no expired promotion logic.');
