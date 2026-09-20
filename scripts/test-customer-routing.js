const fs=require('fs');

const routing=JSON.parse(fs.readFileSync('data/market-routing.json','utf8'));
const cities=JSON.parse(fs.readFileSync('data/cities.json','utf8'));

global.location={hostname:'freereliableappliancepickup.com',pathname:'/'};
global.document={
  addEventListener:()=>{},
  querySelectorAll:()=>[]
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
    ['Cerritos','CA','partner-recruiting','Los Angeles County','priority-california-city','310-774-4304'],
    ['Palmdale','CA','partner-recruiting','Antelope Valley','priority-california-city','310-774-4304'],
    ['San Diego','CA','partner-recruiting','San Diego County','priority-california-city','310-774-4304'],
    ['San Francisco','CA','partner-recruiting','San Francisco Bay Area','priority-california-city','310-774-4304'],
    ['Fresno','CA','partner-recruiting','Central Valley','priority-california-city','310-774-4304'],
    ['Phoenix Metro','AZ','partner-recruiting','Phoenix Metro','regional',null],
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

  console.log(`PASS: ${tests.length} customer routing regression cases, including regional-form labels`);
}

main().catch(err=>{
  console.error(err.stack||err);
  process.exit(1);
});
