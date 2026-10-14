// Execute the production inline checker with its actual DOM field IDs.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('free-pickup-qualification/index.html','utf8');
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const source=scripts.find(s=>s.includes('qualificationCheckerButton'));
assert(source,'Qualification checker script must exist');
const fields={};for(const id of ['type','condition','total','working','companions','result','button']){assert(html.includes('id="qc-'+id+'"'));fields['qc-'+id]={value:'',textContent:'',innerHTML:'',addEventListener:(_,fn)=>fields.click=fn};}
vm.runInNewContext(source,{document:{getElementById:id=>fields[id]}});
const cases=[['major','working',5,1,0,'Choose Multiple'],['multiple','working',5,1,0,'working count should equal'],['major','working',1,1,0,'Likely eligible'],['multiple','mixed',5,4,0,'Likely eligible'],['multiple','mixed',5,3,0,'Below the'],['major','notworking',1,0,0,'generally does not qualify'],['dishwasher','working',3,3,2,'May be reviewed'],['dishwasher','working',2,2,1,'Does not meet'],['microwave','working',1,1,0,'Does not meet'],['multiple','notworking',5,1,0,'Some appliances'],['multiple','mixed',2,2,0,'mixed load must'],['major','unknown',1,0,0,'manual review']];
for(const [type,condition,total,working,companions,expected] of cases){for(const [id,value] of Object.entries({type,condition,total,working,companions}))fields['qc-'+id].value=String(value);fields['qc-result'].textContent='';fields['qc-result'].innerHTML='';fields.click();assert((fields['qc-result'].textContent+fields['qc-result'].innerHTML).includes(expected),JSON.stringify({type,condition,total,working,expected,result:fields['qc-result']}));}
console.log('PASS '+cases.length+' qualification scenarios against production checker');
