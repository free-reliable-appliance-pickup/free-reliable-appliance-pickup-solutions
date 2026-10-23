/* Optional quote-interest field for first-party pickup requests. An empty choice
   is NOT consent to a paid quote. No price, payment, or booking occurs here. */
(function(){
  'use strict';
  const api=window.FreeReliableCustomerRouting;
  if(!api)return;
  document.querySelectorAll('form[action*="formspree.io"]').forEach(form=>{
    if(!api.isCustomerPickupForm(form)||form.querySelector('[name="paid_removal_preference"]'))return;
    const submit=form.querySelector('button[type="submit"],input[type="submit"]');
    if(!submit||!submit.parentNode)return;
    const holder=document.createElement('div');
    holder.className='site-paid-removal-choice';
    holder.style.cssText='display:block;width:100%;box-sizing:border-box;margin:16px 0;padding:14px;border:1px solid #cbded2;border-radius:10px;background:#f6fbf7;color:#17324a;clear:both';
    const label=document.createElement('label');
    label.style.cssText='display:block;font-weight:700;margin-bottom:6px';
    label.textContent='If free pickup is unavailable, would you consider a paid removal quote?';
    const select=document.createElement('select');
    select.name='paid_removal_preference';
    select.style.cssText='display:block;box-sizing:border-box;width:100%;max-width:100%;padding:12px;margin-top:8px;border:1px solid #a5b7ac;border-radius:7px;font:inherit;background:#fff;color:#17324a';
    [['','Please choose an option'],['free_only','Free pickup only — do not offer paid removal'],['quote_ok','Yes — I am open to reviewing a paid removal quote']].forEach(([value,title])=>{
      const option=document.createElement('option');option.value=value;option.textContent=title;select.appendChild(option);
    });
    label.appendChild(select);
    const note=document.createElement('p');
    note.style.cssText='font-size:14px;line-height:1.5;margin:8px 0 0';
    note.textContent='Free pickup is reviewed first. Upstairs, two-person, difficult-access or nonqualifying appliance removal may require a separate quote. No charge or booking without your approval.';
    holder.appendChild(label);holder.appendChild(note);submit.parentNode.insertBefore(holder,submit);
  });
})();
