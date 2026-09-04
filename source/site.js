const header=document.querySelector('.site-header');
const menu=document.querySelector('.menu-btn');
const links=document.querySelector('.nav-links');
const closeDropdown=(drop)=>{const button=drop.querySelector('[data-dropdown-toggle]');const panel=drop.querySelector('.drop-menu');drop.classList.remove('open');button.setAttribute('aria-expanded','false');panel.hidden=true};
const closeMenu=()=>{if(!menu||!links)return;links.classList.remove('open');menu.setAttribute('aria-expanded','false')};
if(menu&&links){menu.addEventListener('click',()=>{const open=links.classList.toggle('open');menu.setAttribute('aria-expanded',open?'true':'false')})}
document.querySelectorAll('[data-dropdown-toggle]').forEach(btn=>btn.addEventListener('click',(event)=>{event.stopPropagation();const drop=btn.closest('.nav-drop');const panel=drop.querySelector('.drop-menu');const open=!drop.classList.contains('open');document.querySelectorAll('.nav-drop.open').forEach(closeDropdown);drop.classList.toggle('open',open);btn.setAttribute('aria-expanded',open?'true':'false');panel.hidden=!open}));
document.addEventListener('click',(event)=>{document.querySelectorAll('.nav-drop.open').forEach(drop=>{if(!drop.contains(event.target))closeDropdown(drop)});if(menu&&links&&links.classList.contains('open')&&!links.contains(event.target)&&!menu.contains(event.target))closeMenu()});
document.addEventListener('keydown',(event)=>{if(event.key!=='Escape')return;document.querySelectorAll('.nav-drop.open').forEach(drop=>{closeDropdown(drop);drop.querySelector('[data-dropdown-toggle]').focus()});if(menu&&links&&links.classList.contains('open')){closeMenu();menu.focus()}});
document.addEventListener('scroll',()=>header&&header.classList.toggle('scrolled',window.scrollY>8),{passive:true});
document.querySelectorAll('.faq button').forEach(btn=>btn.addEventListener('click',()=>{const item=btn.closest('.faq');const panel=document.getElementById(btn.getAttribute('aria-controls'));const open=!item.classList.contains('open');item.classList.toggle('open',open);btn.setAttribute('aria-expanded',open?'true':'false');if(panel)panel.hidden=!open;const icon=btn.querySelector('[aria-hidden="true"]');if(icon)icon.textContent=open?'−':'+'}));
const lang=document.documentElement.lang;try{localStorage.setItem('scout-language',lang)}catch(e){}

const consentKey='scout-consent-v1';
const disclosure=document.querySelector('[data-privacy-disclosure]');
const essentialOnly={essential:true,analytics:false,version:1};
const readConsent=()=>{try{const parsed=JSON.parse(localStorage.getItem(consentKey));return parsed&&parsed.version===1&&parsed.essential===true&&parsed.analytics===false?essentialOnly:null}catch(error){return null}};
if(disclosure){
  disclosure.hidden=Boolean(readConsent());
  disclosure.querySelector('[data-privacy-accept]')?.addEventListener('click',()=>{
    try{localStorage.setItem(consentKey,JSON.stringify(essentialOnly))}catch(error){}
    disclosure.hidden=true;
  });
  document.querySelectorAll('[data-privacy-open]').forEach(button=>button.addEventListener('click',()=>{
    disclosure.hidden=false;
    disclosure.querySelector('[data-privacy-accept]')?.focus();
  }));
}

window.scoutTurnstileSuccess=(token)=>{
  const input=document.querySelector('[data-turnstile-token]');
  if(input)input.value=token;
};
window.scoutTurnstileExpired=()=>{
  const input=document.querySelector('[data-turnstile-token]');
  if(input)input.value='';
};

const formMessages={
  en:{pending:'Sending securely…',generic:'We could not send your enquiry. Please try again or contact us by email.',invalid_form:'Please check the required fields and the privacy acknowledgement.',turnstile_failed:'The security check was not completed. Please try again.',delivery_failed:'Delivery is temporarily unavailable. Please contact us by email.'},
  he:{pending:'הפנייה נשלחת באופן מאובטח…',generic:'לא הצלחנו לשלוח את הפנייה. נסו שוב או פנו אלינו בדוא״ל.',invalid_form:'יש לבדוק את שדות החובה ואת אישור הודעת הפרטיות.',turnstile_failed:'בדיקת האבטחה לא הושלמה. נסו שוב.',delivery_failed:'שירות השליחה אינו זמין זמנית. ניתן לפנות אלינו בדוא״ל.'}
};
document.querySelectorAll('.contact-form').forEach(form=>form.addEventListener('submit',async(event)=>{
  event.preventDefault();
  const button=form.querySelector('button[type="submit"]');
  const status=form.querySelector('.form-status');
  const messages=formMessages[form.elements.lang?.value]||formMessages.en;
  if(!form.reportValidity())return;
  button.disabled=true;
  button.textContent=messages.pending;
  status.textContent='';
  try{
    const response=await fetch(form.action,{method:'POST',body:new FormData(form),headers:{Accept:'application/json'}});
    const payload=await response.json().catch(()=>({}));
    if(!response.ok||payload.ok!==true)throw Object.assign(new Error('submission_failed'),{code:payload.code||'generic'});
    window.location.assign(`/${form.elements.lang.value}/thank-you/`);
  }catch(error){
    status.textContent=messages[error.code]||messages.generic;
    status.focus();
    button.disabled=false;
    button.textContent=button.dataset.idleLabel;
    if(window.turnstile){try{window.turnstile.reset()}catch(resetError){}}
    window.scoutTurnstileExpired();
  }
}));
