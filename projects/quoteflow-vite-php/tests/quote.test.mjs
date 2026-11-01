import {test} from 'node:test'; import assert from 'node:assert/strict'; import {calculateQuote} from '../src/quote.js';
test('calculates totals',()=>{const x=calculateQuote([{description:'Support',quantity:2,unitPrice:15}],10);assert.equal(x.subtotal,30);assert.equal(x.tax,3);assert.equal(x.total,33)});
test('validates invalid inputs',()=>{assert.throws(()=>calculateQuote([{description:'',quantity:1,unitPrice:3}]));assert.throws(()=>calculateQuote([],101))});
