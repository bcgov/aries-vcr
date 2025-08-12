/* All rights reserved, unlicensed. */
const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');

const ajv = new Ajv({ allErrors: true, strict: false });

function load(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

const base = path.join(__dirname, '..');
const schema1 = load(path.join(base, 'schemas', 'MentalWellnessSessionCredential.json'));
const schema2 = load(path.join(base, 'schemas', 'PractitionerAttestationCredential.json'));

const sample1 = load(path.join(__dirname, 'sample_MentalWellnessSessionCredential.json'));
const sample2 = load(path.join(__dirname, 'sample_PractitionerAttestationCredential.json'));

const v1 = ajv.compile(schema1);
const v2 = ajv.compile(schema2);

if (!v1(sample1)) {
  console.error('MentalWellnessSessionCredential validation failed:', v1.errors);
  process.exit(1);
}

if (!v2(sample2)) {
  console.error('PractitionerAttestationCredential validation failed:', v2.errors);
  process.exit(1);
}

console.log('All healthcare VC samples passed schema validation.');
