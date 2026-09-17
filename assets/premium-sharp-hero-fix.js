/* Washer/dryer hero clarity override. Use only full-size real JPEGs; never use tiny WebP hero sprites. */
(function(){
'use strict';
const photos=[
'real-laundry-pickup-1.jpg',
'real-laundry-pickup-2.jpg',
'real-laundry-pickup-3.jpg',
'real-laundry-pickup-4.jpg',
'real-laundry-pickup-5.jpg'
];
function base(){const h=(location.hostname||'').toLowerCase();if(h.endsWith('.github.io')){const p=(location.pathname||'/').split('/').filter(Boolean)[0];return p?'/'+p+'/':'/';}return '/';}
function path(){let p=location.pathname||'/',b=base();if(b!=='/'&&p.startsWith(b.slice(0,-1)))p=p.slice(b.length-1)||'/';if(!p.startsWith('/'))p='/'+p;if(!p.endsWith('/'))p+='/';return p;}
function cityLabel(){const field=document.querySelector('form input[name="city"]');if(field&&field.value)return field.value.trim();const h1=document.querySelector('.site-hero h1');return h1?h1.textContent.replace(/Free Washer\s*&\s*Dryer\s*Pickup\s*in\s*/i,'').replace(/,?\s*CA\s*$/i,'').trim():'';}
function styleHero(hero){const art=hero.closest('.site-hero-art');if(art){art.style.setProperty('background','none','important');art.style.setProperty('background-image','none','important');art.style.setProperty('aspect-ratio','auto','important');art.style.setProperty('overflow','visible','important');art.style.setProperty('width','auto','important');art.style.setProperty('box-shadow','none','important');}
hero.removeAttribute('width');hero.removeAttribute('height');hero.loading='eager';hero.fetchPriority='high';hero.decoding='async';hero.style.setProperty('opacity','1','important');hero.style.setProperty('position','relative','important');hero.style.setProperty('inset','auto','important');hero.style.setProperty('display','block','important');hero.style.setProperty('width','auto','important');hero.style.setProperty('height','auto','important');hero.style.setProperty('max-width','min(100%,520px)','important');hero.style.setProperty('max-height','620px','important');hero.style.setProperty('object-fit','contain','important');hero.style.setProperty('image-rendering','auto','important');hero.style.setProperty('background','#fff','important');hero.style.setProperty('border-radius','16px','important');hero.style.setProperty('box-shadow','0 12px 28px rgba(0,61,96,.12)','important');}
function apply(){const p=path();if(!/-washer-dryer-pickup\/$/.test(p))return;const hero=document.querySelector('.site-hero-art img');if(!hero)return;let hash=0;for(let i=0;i<p.length;i++)hash=(hash*31+p.charCodeAt(i))>>>0;const file=photos[hash%photos.length];hero.src=base()+'assets/laundry/'+file+'?full-res=20260916-1';const city=cityLabel();if(city)hero.alt='Real washer and dryer set for pickup in '+city;hero.dataset.fullResolutionHero='1';styleHero(hero);}
function run(){apply();requestAnimationFrame(apply);setTimeout(apply,250);setTimeout(apply,900);}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
window.addEventListener('load',run);
})();
