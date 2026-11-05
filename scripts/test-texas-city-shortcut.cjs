/* Texas quick-city no-browser behavioral regression. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('texas-appliance-pickup/index.html','utf8');
assert.match(html,/<section id="texas-city-shortcut"/);
assert.match(html,/<button id="texas-quick-continue" type="button"/);
assert.match(html,/<datalist id="texas-city-suggestions"/);
assert.match(html,/<script src="\/assets\/texas-city-shortcut\.js" defer><\/script>/);
assert.equal((html.match(/<form\b/g)||[]).length,1,'no extra lead form');
assert.match(html,/<meta name="robots" content="index, follow/);
const nodes={};
function el(x={}){return Object.assign({value:'',textContent:'',children:[],handlers:{},focus(){this.focused=true},addEventListener(k,fn){this.handlers[k]=fn},dispatchEvent(e){(this.events||(this.events=[])).push(e.type)},appendChild(n){this.children.push(n)}},x)}
const input=el(),button=el(),list=el(),status=el(),city=el(),name=el();
const request=el({querySelector(s){if(s==='form [name="city"]')return city;if(s==='form [name="name"]')return name;return null},scrollIntoView(){this.scrolled=true}});
Object.assign(nodes,{'texas-quick-city':input,'texas-quick-continue':button,'texas-city-suggestions':list,'texas-quick-status':status,'request':request});
const priorityNames=[...html.matchAll(/<li><a href="#request" data-texas-priority-city="([^"]+)">\\1<\\/a><\\/li>/g)].map(x=>x[1]);
assert.deepEqual(priorityNames,["Houston","San Antonio","Dallas","Fort Worth","Austin","El Paso","Arlington","Corpus Christi","Plano","Lubbock","Laredo","Irving","Garland","Frisco","McKinney","Grand Prairie","Amarillo","Brownsville","Denton","Killeen"],'2025 Texas population order');
const priorityLinks=priorityNames.map(name=>el({getAttribute(key){return key==='data-texas-priority-city'?name:null}}));
const document={
 readyState:'complete',getElementById(id){return nodes[id]||null},
 querySelector(q){return q.includes('texas-city-shortcut.js')?{src:'https://freereliableappliancepickup.com/assets/texas-city-shortcut.js'}:null},
 querySelectorAll(q){return q==='[data-texas-priority-city]'?priorityLinks:[]},
 createElement(tag){return el({tagName:tag})},
};
const catalog=JSON.parse(fs.readFileSync('data/cities.json','utf8'));
const ctx={document,Event:class{constructor(type){this.type=type}},URL,Set,fetch:async()=>({ok:true,json:async()=>catalog})};
vm.runInNewContext(fs.readFileSync('assets/texas-city-shortcut.js','utf8'),ctx);
(async()=>{
 await new Promise(resolve=>setImmediate(resolve));
 assert(list.children.length>=148,'offers the mapped Texas cities');
 input.value=' Katy ';
 button.handlers.click();
 assert.equal(city.value,'Katy','copies the actual Texas city');
 assert.deepEqual(city.events,['input','change']);
 assert(request.scrolled,'request scrolled into view');
 assert(name.focused,'customer name receives focus');
 input.value='';
 button.handlers.click();
 assert.equal(city.value,'Katy','blank quick entry does not overwrite city');
 assert.match(status.textContent,/Please enter/);
 input.value='An Unlisted Texas Community';
 button.handlers.click();
 assert.equal(city.value,'An Unlisted Texas Community','unlisted city accepted');
 const corpus=priorityLinks[7];
 let prevented=false;
 corpus.handlers.click({preventDefault(){prevented=true}});
 assert(prevented,'priority city intercepts in-page link when JS is active');
 assert.equal(city.value,'Corpus Christi','priority city links prefill the existing request city');
 assert.equal(input.value,'Corpus Christi','chosen priority city is visible in quick city input');
 priorityLinks[19].handlers.click({preventDefault(){}});
 assert.equal(city.value,'Killeen','last priority city also works');
 assert.equal((html.match(/<img\\b/gi)||[]).length,2,'only brand logo and one garage photo');
 console.log('PASS: Texas quick-city shortcut, 148 suggestions, unlisted cities, form preservation');
})().catch(e=>{console.error(e);process.exit(1)});
