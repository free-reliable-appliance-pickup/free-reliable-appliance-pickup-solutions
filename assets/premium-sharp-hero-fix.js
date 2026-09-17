/* Washer/dryer hero clarity override. Exact user-provided city photos always win. Never recompress, resize, crop, rotate, or convert image bytes. */
(function(){
'use strict';
const fallbackPhotos=[
'real-laundry-pickup-1.jpg',
'real-laundry-pickup-2.jpg',
'real-laundry-pickup-3.jpg',
'real-laundry-pickup-4.jpg',
'real-laundry-pickup-5.jpg'
];
function base(){const h=(location.hostname||'').toLowerCase();if(h.endsWith('.github.io')){const p=(location.pathname||'/').split('/').filter(Boolean)[0];return p?'/'+p+'/':'/';}return '/';}
function pagePath(){let p=location.pathname||'/',b=base();if(b!=='/'&&p.startsWith(b.slice(0,-1)))p=p.slice(b.length-1)||'/';if(!p.startsWith('/'))p='/'+p;if(!p.endsWith('/'))p+='/';return p;}
function cityLabel(){const field=document.querySelector('form input[name="city"]');if(field&&field.value)return field.value.trim();const h1=document.querySelector('.site-hero h1');return h1?h1.textContent.replace(/Free Washer\s*&\s*Dryer\s*Pickup\s*in\s*/i,'').replace(/,?\s*CA\s*$/i,'').trim():'';}
function styleHero(hero){const art=hero.closest('.site-hero-art');if(art){art.style.setProperty('background','none','important');art.style.setProperty('background-image','none','important');art.style.setProperty('aspect-ratio','auto','important');art.style.setProperty('overflow','visible','important');art.style.setProperty('width','auto','important');art.style.setProperty('box-shadow','none','important');}hero.removeAttribute('width');hero.removeAttribute('height');hero.loading='eager';hero.fetchPriority='high';hero.decoding='async';hero.style.setProperty('opacity','1','important');hero.style.setProperty('position','relative','important');hero.style.setProperty('inset','auto','important');hero.style.setProperty('display','block','important');hero.style.setProperty('width','auto','important');hero.style.setProperty('height','auto','important');hero.style.setProperty('max-width','min(100%,520px)','important');hero.style.setProperty('max-height','620px','important');hero.style.setProperty('object-fit','contain','important');hero.style.setProperty('image-rendering','auto','important');hero.style.setProperty('background','#fff','important');hero.style.setProperty('border-radius','16px','important');hero.style.setProperty('box-shadow','0 12px 28px rgba(0,61,96,.12)','important');}
function hero(){return document.querySelector('.site-hero-art img');}
function isExistingOriginal(img){const raw=String(img&&img.getAttribute('src')||'');return raw.includes('/assets/laundry/original-user-heroes/')||raw.includes('original-fullres=')||raw.includes('exact-user-hero=');}
function applyFallback(){const p=pagePath();if(!/-washer-dryer-pickup\/$/.test(p))return;const img=hero();if(!img||img.dataset.userProvidedHero==='1')return;if(isExistingOriginal(img)){img.dataset.userProvidedHero='1';img.dataset.fullResolutionHero='1';delete img.dataset.fullResolutionFallback;styleHero(img);return;}let hash=0;for(let i=0;i<p.length;i++)hash=(hash*31+p.charCodeAt(i))>>>0;const file=fallbackPhotos[hash%fallbackPhotos.length];img.src=base()+'assets/laundry/'+file+'?full-res-fallback=20260917c';const city=cityLabel();if(city)img.alt='Real washer and dryer set for pickup in '+city;img.dataset.fullResolutionFallback='1';styleHero(img);}
async function applyExactCityHero(){const p=pagePath();if(!/-washer-dryer-pickup\/$/.test(p))return;const img=hero();if(!img)return;try{const res=await fetch(base()+'assets/premium-user-heroes.json?exact-user-heroes=20260917c',{cache:'no-store'});if(!res.ok)return;const map=await res.json();const cfg=map[p];if(!cfg)return;if(cfg.src){img.src=base()+cfg.src+'?exact-user-hero=20260917c';}else if(Array.isArray(cfg.parts)&&cfg.parts.length){const chunks=await Promise.all(cfg.parts.map(part=>fetch(base()+part+'?exact-user-hero=20260917c',{cache:'force-cache'}).then(r=>{if(!r.ok)throw new Error('hero part');return r.text();})));img.src='data:'+(cfg.mime||'image/jpeg')+';base64,'+chunks.map(s=>s.trim()).join('');}else{return;}if(cfg.alt)img.alt=cfg.alt;img.dataset.userProvidedHero='1';img.dataset.fullResolutionHero='1';delete img.dataset.fullResolutionFallback;styleHero(img);}catch(e){}}
function run(){applyFallback();applyExactCityHero();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
window.addEventListener('load',run);
setTimeout(run,250);
setTimeout(run,900);
})();
