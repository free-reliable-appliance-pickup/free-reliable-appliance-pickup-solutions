const fs=require('fs');

const routing=JSON.parse(fs.readFileSync('data/market-routing.json','utf8'));
const cities=JSON.parse(fs.readFileSync('data/cities.json','utf8'));

global.location={hostname:'freereliableappliancepickup.com',pathname:'/'};
global.document={
  addEventListener:()=>{},
  querySelectorAll:()=>[],
  querySelector:(selector)=>selector==='script[data-premium-sharp-hero]'?{}:null
};
global.window={};
global.fetch=async function(url){
  if(String(url).includes('market-routing.json')) return {ok:true,json:async()=>routing};
  if(String(url).includes('cities.json')) return {ok:true,json:async()=>cities};
  return {ok:false,json:async()=>({})};
};

const source=fs.readFileSync('assets/customer-routing.js','utf8');
eval(source);

function assertEqual(actual,expected,label){
  if(actual!==expected){
    throw new Error(`${label}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

async function main(){
  const api=window.FreeReliableCustomerRouting;
  if(!api) throw new Error('Customer routing API was not exposed');
  await api.load();

  const tests=[
    ['Portland','OR','direct','Portland Metro','exact-city','503-868-4455'],
    ['Beaverton','OR','direct','Portland Metro','regional','503-868-4455'],
    ['Denver Metro','CO','direct','Denver Metro','regional','720-604-7498'],
    ['Los Angeles County','CA','partner-recruiting','Los Angeles County','regional','310-774-4304'],
    ['Inland Empire','CA','partner-recruiting','Inland Empire','regional','909-375-6685'],
    ['Orange County','CA','partner-recruiting','Orange County','regional','909-375-6685'],
    ['Riverside County','CA','partner-recruiting','Riverside County','regional','909-375-6685'],
    ['Perris','CA','partner-recruiting','Riverside County','priority-california-city','909-375-6685'],
    ['Victorville','CA','partner-recruiting','Victorville Valley','priority-california-city','909-375-6685'],
    ['Palm Desert','CA','partner-recruiting','Coachella Valley','priority-california-city','909-375-6685'],
    ['Alhambra','CA','partner-recruiting','San Gabriel Valley','priority-california-city','909-375-6685'],
    ['Santa Ana','CA','partner-recruiting','Orange County','priority-california-city','909-375-6685'],
    // Customer-confirmed Oct 11: these three cities use 909 even though the county hub remains 310.
    ['La Mirada','CA','partner-recruiting','Los Angeles County','priority-california-city','909-375-6685'],
    ['Cerritos','CA','partner-recruiting','Los Angeles County','priority-california-city','909-375-6685'],
    ['Pico Rivera','CA','partner-recruiting','Los Angeles County','priority-california-city','909-375-6685'],
    ['Bell','CA','partner-recruiting','Los Angeles County','priority-california-city','310-774-4304'],
    ['Palmdale','CA','partner-recruiting','Antelope Valley','priority-california-city','310-774-4304'],
    ['San Diego','CA','partner-recruiting','San Diego County','priority-california-city','310-774-4304'],
    ['San Francisco','CA','partner-recruiting','San Francisco Bay Area','priority-california-city','310-774-4304'],
    ['Fresno','CA','partner-recruiting','Central Valley','priority-california-city','310-774-4304'],
    ['Phoenix Metro','AZ','partner-recruiting','Phoenix Metro','regional','602-726-7552'],
    ['Las Vegas Valley','NV','partner-recruiting','Las Vegas Valley','regional',null],
    ['Columbus','OH','request-only','Ohio statewide intake','statewide',null]
  ];

  for(const [city,state,status,region,level,phone] of tests){
    const result=api.classify(city,state);
    assertEqual(result.status,status,`${city}, ${state} status`);
    assertEqual(result.region,region,`${city}, ${state} region`);
    assertEqual(result.resolution_level,level,`${city}, ${state} resolution`);
    assertEqual(result.phone??null,phone,`${city}, ${state} phone`);
  }

  const laDecision=api.routingDecision(api.classify('Los Angeles County','CA'));
  assertEqual(laDecision.decision,'RECRUITING_QUEUE','Los Angeles County decision');
  const denverDecision=api.routingDecision(api.classify('Denver Metro','CO'));
  assertEqual(denverDecision.decision,'DIRECT_OPERATION','Denver Metro decision');

  // California legacy forms may contain plural "appliances" instead of singular "appliance".
  // Confirm these still obtain routing metadata and page attribution without changing existing values.
  global.document.createElement=tag=>({tagName:tag,type:'',name:'',value:''});
  function mockForm(fields){
    const nodes={};
    for(const [name,value] of Object.entries(fields)) nodes[name]={name,value,type:name==='source_page'?'hidden':'text'};
    return {
      nodes,
      querySelector(selector){
        const m=String(selector).match(/\[name="([^"]+)"\]/);
        if(m) return this.nodes[m[1]]||null;
        if(String(selector).startsWith('#')) return this.nodes[String(selector).slice(1)]||null;
        return null;
      },
      appendChild(node){this.nodes[node.name]=node;return node;}
    };
  }
  // Forms across markets submit different labels for non-fully-working appliances.
  // Every reported problem must receive the explicit partner-review gate.
  const conditionCases=[
    ['Fully Working',false],
    ['Working With Issues',true],
    ['Working, but has a problem (explain below)',true],
    ['Needs Repair',true],
    ['Needs minor repair',true],
    ['Not Working',true],
    ['Unknown',true],
    ['Mixed Load',true],
    ['Mixed Load - Mixed Conditions',true],
    ['Broken',true]
  ];
  for(const [condition,review] of conditionCases){
    const form=mockForm({city:'Pico Rivera',state:'California',appliance:'Washer',condition});
    api.qualify(form);
    const expected=review?'REVIEW REPORTED CONDITION WITH PARTNER BEFORE DISPATCH':'CONFIRM CONDITION AND AVAILABILITY BEFORE DISPATCH';
    assertEqual(form.nodes['Dispatch Condition Gate'].value,expected,'Condition review gate: '+condition);
    assertEqual(form.nodes['Routing Phone'].value,'909-375-6685','Condition fix preserves customer routing');
  }
  console.log('PASS: '+conditionCases.length+' actual appliance-condition dispatch labels');

  // Regression: a real Washington intake option ("Mixed load - majority working")
  // was previously rewritten to Unknown when the shared browser enhancement ran.
  // Exercise the enhancement itself using a minimal browser form mock.
  const conditionEnhancementStart=source.indexOf('function enhanceApplianceConditionIntake()');
  const conditionEnhancementEnd=source.indexOf('\nfunction enhanceRequestNextSteps()',conditionEnhancementStart);
  if(conditionEnhancementStart<0||conditionEnhancementEnd<=conditionEnhancementStart){
    throw new Error('Unable to find shared condition enhancement for regression test');
  }
  const conditionEnhancer=new Function('document',source.slice(conditionEnhancementStart,conditionEnhancementEnd)+'\nreturn enhanceApplianceConditionIntake;');
  function checkConditionPreservation(initialOptions,selectedValue,expectedOptionCount){
    const listener={};
    const select={
      value:selectedValue,
      options:initialOptions.map(value=>({value})),
      appendChild(option){this.options.push(option);},
      addEventListener(type,callback){listener[type]=callback;},
      closest(){return null;},
      insertAdjacentElement(_position,label){this.detailsLabel=label;}
    };
    const documentMock={
      querySelectorAll:()=>[{
        querySelector(selector){
          if(selector==='select[name="condition"]')return select;
          if(selector==='[name="condition_details"]')return null;
          return null;
        }
      }],
      createElement(tag){
        return {
          tagName:tag,
          style:{},
          appendChild(child){this.child=child;},
          setAttribute(key,value){this[key]=value;}
        };
      }
    };
    conditionEnhancer(documentMock)();
    assertEqual(select.value,selectedValue,'Preserve actual selected condition');
    assertEqual(select.options.length,expectedOptionCount,'Do not replace/delete original condition options');
    assertEqual(select.options.some(x=>x.value.toLowerCase()==='mixed load - majority working'),true,'Mixed load remains available');
    assertEqual(select.options.some(x=>x.value==='Working With Issues'),true,'Working-with-issues choice available');
    assertEqual(select.detailsLabel.child.required,true,'Mixed load requires item-by-item details');
    select.value='Fully working';
    listener.change();
    assertEqual(select.detailsLabel.child.required,false,'Fully working does not require fault details');
    select.value='Needs minor repair';
    listener.change();
    assertEqual(select.detailsLabel.child.required,true,'Repair condition requires fault details');
  }
  checkConditionPreservation(
    ['', 'Fully working','Needs minor repair','Not working','Unknown','Mixed load - majority working'],
    'Mixed load - majority working',7
  );
  console.log('PASS: mixed appliance load preserved in the live form enhancement');


  global.location.pathname='/victorville-appliance-pickup/';
  const legacy=mockForm({city:'Victorville',state:'California',appliances:'Washer and dryer',condition:'Fully Working'});
  api.qualify(legacy);
  assertEqual(legacy.nodes.source_page.value,'victorville-appliance-pickup','Legacy form gains page source');
  assertEqual(legacy.nodes['Routing Region'].value,'Victorville Valley','Legacy California region');
  assertEqual(legacy.nodes['Routing Phone'].value,'909-375-6685','Legacy California phone');
  assertEqual(legacy.nodes['Routing Decision'].value,'RECRUITING_QUEUE','Legacy request never promises service');
  assertEqual(legacy.nodes['Qualification Snapshot'].value,'Washer and dryer | Fully Working','Legacy plural appliances captured');
  global.location.pathname='/fontana-appliance-pickup/';
  const existing=mockForm({city:'Fontana',state:'California',appliance:'Refrigerator',condition:'Fully Working',source_page:'original-campaign-source'});
  api.qualify(existing);
  assertEqual(existing.nodes.source_page.value,'original-campaign-source','Existing page source preserved');
  // Verify that older California city/laundry forms receive attribution only
  // when the page slug and state are a known, correct location.
  global.location.pathname='/alhambra-washer-dryer-pickup/';
  const missingCity=mockForm({state:'California',appliance:'Washer / Dryer',condition:'Fully Working'});
  assertEqual(api.isCustomerPickupForm(missingCity),true,'City-less Alhambra pickup qualifies for routing');
  api.ensureRequestAttribution(missingCity);
  assertEqual(missingCity.nodes.city.value,'Alhambra','City inferred from real Alhambra CA route');
  assertEqual(missingCity.nodes.source_page.value,'alhambra-washer-dryer-pickup','City-less source captured');
  api.qualify(missingCity);
  assertEqual(missingCity.nodes['Routing Phone'].value,'909-375-6685','Alhambra partner-recruiting phone');
  assertEqual(missingCity.nodes['Routing Decision'].value,'RECRUITING_QUEUE','No pickup promise from inferred city');

  global.location.pathname='/bell-washer-dryer-pickup/';
  const bell=mockForm({state:'CA',appliances:'Washer and dryer',condition:'Unknown'});
  api.ensureRequestAttribution(bell);
  assertEqual(bell.nodes.city.value,'Bell','Southeast LA pickup city inferred');
  api.qualify(bell);
  assertEqual(bell.nodes['Routing Phone'].value,'310-774-4304','Bell regional contact mapping');

  // Keep city-specific 909 dispatch even for older laundry HTML that omits city.
  for(const [slug,city] of [['la-mirada','La Mirada'],['cerritos','Cerritos'],['pico-rivera','Pico Rivera']]){
    global.location.pathname='/'+slug+'-washer-dryer-pickup/';
    const form=mockForm({state:'California',appliance:'Washer and Dryer Set',condition:'Fully Working'});
    api.ensureRequestAttribution(form);
    assertEqual(form.nodes.city.value,city,city+' laundry inferred verified city');
    api.qualify(form);
    assertEqual(form.nodes['Routing Phone'].value,'909-375-6685',city+' laundry request routes to 909');
    assertEqual(form.nodes.source_page.value,slug+'-washer-dryer-pickup',city+' original source preserved');
    assertEqual(form.nodes['Routing Decision'].value,'RECRUITING_QUEUE',city+' does not promise pickup');
  }

  global.location.pathname='/denver-refrigerator-pickup/';
  const denver=mockForm({state:'Colorado',appliance:'Refrigerator'});
  api.ensureRequestAttribution(denver);
  assertEqual(denver.nodes.city.value,'Denver','Verified direct-market city inferred');
  api.qualify(denver);
  assertEqual(denver.nodes['Routing Decision'].value,'DIRECT_OPERATION','Real direct market retained');

  global.location.pathname='/california-washer-dryer-pickup/';
  const statewide=mockForm({state:'California',appliance:'Washer'});
  api.ensureRequestAttribution(statewide);
  assertEqual(!!statewide.nodes.city,false,'Never infer California as a city');
  assertEqual(!!statewide.nodes.source_page,true,'Regional form still gets provenance');

  global.location.pathname='/clovis-appliance-pickup/';
  const crossCity=mockForm({city:'Fresno',state:'CA',appliance:'Stove',source_page:'verified-campaign'});
  api.ensureRequestAttribution(crossCity);
  assertEqual(crossCity.nodes.city.value,'Fresno','Explicit customer pickup city not overwritten');
  assertEqual(crossCity.nodes.source_page.value,'verified-campaign','Existing campaign attribution not overwritten');

  global.location.pathname='/nonexistent-city-washer-dryer-pickup/';
  const unknown=mockForm({state:'CA',appliance:'Washer'});
  api.ensureRequestAttribution(unknown);
  assertEqual(!!unknown.nodes.city,false,'Unverified city slug is not fabricated');
  global.location.pathname='/';

  console.log('PASS: legacy form alias, page attribution, confirmed route metadata and preexisting attribution');

  console.log(`PASS: ${tests.length} customer routing regression cases, including regional-form labels`);
}

main().catch(err=>{
  console.error(err.stack||err);
  process.exit(1);
});
