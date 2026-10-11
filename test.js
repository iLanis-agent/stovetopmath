const E = require('./engine.js');
const cases = require('./expected.json');
let pass = 0, fail = 0;
function chk(name, cond) { if (cond) pass++; else { fail++; console.log('FAIL', name); } }
cases.forEach((c, i) => {
  let actual, render;
  if (c.fn === 'boilPlan') { actual = E.boilPlan(...c.args); render = actual.error || E.renderBoil(actual); }
  else if (c.fn === 'lidPlan') { actual = E.lidPlan(...c.args); render = actual.error || E.renderLid(actual); }
  else { actual = E.yearPlan(...c.args); render = actual.error || E.renderYear(actual); }
  chk(i + ':' + c.fn + ':result', JSON.stringify(actual) === JSON.stringify(c.result));
  chk(i + ':' + c.fn + ':render', render === c.render);
  chk(i + ':' + c.fn + ':errorflag', (!!actual.error) === c.isError);
});
console.log(cases.length + ' cases, ' + pass + ' checks green, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
