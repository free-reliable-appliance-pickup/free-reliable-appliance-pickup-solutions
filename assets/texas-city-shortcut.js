/* Optional Texas city shortcut, never a claim of service availability. */
(function(){
  'use strict';
  function init(){
    const input=document.getElementById('texas-quick-city');
    const button=document.getElementById('texas-quick-continue');
    const list=document.getElementById('texas-city-suggestions');
    const status=document.getElementById('texas-quick-status');
    const request=document.getElementById('request');
    const city=request&&request.querySelector('form [name="city"]');
    if(!input||!button||!list||!status||!request||!city)return;
    function submitCity(){
      const entered=input.value.trim().replace(/\s+/g,' ').slice(0,100);
      if(!entered){
        status.textContent='Please enter your actual Texas pickup city first.';
        input.focus();
        return;
      }
      city.value=entered;
      city.dispatchEvent(new Event('input',{bubbles:true}));
      city.dispatchEvent(new Event('change',{bubbles:true}));
      status.textContent='City added: '+entered+'. Complete the request form to check eligibility.';
      if(request.scrollIntoView)request.scrollIntoView({behavior:'smooth',block:'start'});
      const name=request.querySelector('form [name="name"]');
      if(name&&name.focus)name.focus({preventScroll:true});
    }
    button.addEventListener('click',submitCity);
    input.addEventListener('keydown',function(event){
      if(event.key==='Enter'){event.preventDefault();submitCity();}
    });
    /* Requested-priority links use the same existing request form and qualification. */
    document.querySelectorAll('[data-texas-priority-city]').forEach(function(link){
      link.addEventListener('click',function(event){
        event.preventDefault();
        const chosen=link.getAttribute('data-texas-priority-city');
        if(!chosen)return;
        input.value=chosen;
        submitCity();
      });
    });
    const script=document.querySelector('script[src*="texas-city-shortcut.js"]');
    const url=script&&script.src?new URL('../data/cities.json',script.src).toString():null;
    if(!url||typeof fetch!=='function')return;
    fetch(url,{cache:'no-store'}).then(function(response){
      if(!response.ok)throw Error('City suggestions unavailable');
      return response.json();
    }).then(function(data){
      if(!Array.isArray(data.cities))return;
      const names=Array.from(new Set(data.cities.filter(function(row){
        return row&&row.state_code==='TX'&&typeof row.city==='string';
      }).map(function(row){return row.city.trim();}).filter(Boolean)))
        .sort(function(a,b){return a.localeCompare(b,'en');});
      names.forEach(function(name){
        const option=document.createElement('option');
        option.value=name;
        list.appendChild(option);
      });
    }).catch(function(){
      /* Every Texas city can still be typed, even if suggestions fail. */
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});
  else init();
})();
