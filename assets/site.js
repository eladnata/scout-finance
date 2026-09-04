
const header=document.querySelector('.site-header');
const menu=document.querySelector('.menu-btn');
const links=document.querySelector('.nav-links');
if(menu){menu.addEventListener('click',()=>{const open=links.classList.toggle('open');menu.setAttribute('aria-expanded',open?'true':'false')})}
document.querySelectorAll('.nav-drop>button').forEach(btn=>btn.addEventListener('click',(e)=>{e.stopPropagation();btn.parentElement.classList.toggle('open')}));
document.addEventListener('click',()=>document.querySelectorAll('.nav-drop').forEach(d=>d.classList.remove('open')));
document.addEventListener('scroll',()=>header&&header.classList.toggle('scrolled',window.scrollY>8),{passive:true});
document.querySelectorAll('.faq button').forEach(btn=>btn.addEventListener('click',()=>{const item=btn.closest('.faq');const open=item.classList.toggle('open');btn.setAttribute('aria-expanded',open?'true':'false');btn.querySelector('span:last-child').textContent=open?'−':'+'}));
const lang=document.documentElement.lang;try{localStorage.setItem('scout-language',lang)}catch(e){}
