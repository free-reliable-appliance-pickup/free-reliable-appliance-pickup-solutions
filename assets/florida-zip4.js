/* Florida request-only city forms: extend five-digit ZIP validation to ZIP+4. */
(function(){
'use strict';
function improve(){
  if(!/^\/[a-z0-9-]+-fl-(?:appliance|washer-dryer|refrigerator|freezer|stove-oven)-pickup\/$/.test(location.pathname))return;
  document.querySelectorAll('form[action*="formspree.io"]').forEach(form=>{
    const zip=form.querySelector('input[name="zip"]');
    if(!zip||zip.getAttribute('pattern')!=='[0-9]{5}')return;
    zip.setAttribute('pattern','[0-9]{5}(-[0-9]{4})?');
    zip.setAttribute('minlength','5');
    zip.setAttribute('maxlength','10');
    zip.setAttribute('title','Enter a five-digit ZIP or ZIP+4 (e.g. 33101-1234)');
    const label=zip.closest('label');
    if(label&&label.firstChild&&label.firstChild.nodeType===3){
      label.firstChild.textContent='ZIP code (5 digits or ZIP+4)';
    }
  });
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',improve,{once:true});
else improve();
})();