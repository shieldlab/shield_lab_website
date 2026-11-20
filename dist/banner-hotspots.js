(() => {
 const group=document.querySelector('.banner-hotspots'); if(!group)return;
 const items=[...group.querySelectorAll('.research-hotspot')];
 const close=()=>items.forEach(item=>{item.querySelector('button').setAttribute('aria-expanded','false');item.querySelector('.hotspot-card').hidden=true;});
 const open=item=>{close();item.querySelector('button').setAttribute('aria-expanded','true');item.querySelector('.hotspot-card').hidden=false;};
 items.forEach(item=>{const button=item.querySelector('button');let touch=false;
 item.addEventListener('pointerenter',e=>{if(e.pointerType!=='touch')open(item);});
 item.addEventListener('pointerleave',e=>{if(e.pointerType!=='touch'&&!item.contains(document.activeElement))close();});
 button.addEventListener('pointerdown',e=>{touch=e.pointerType==='touch';});
 button.addEventListener('focus',()=>{if(!touch)open(item);});
 button.addEventListener('click',()=>{if(touch){if(button.getAttribute('aria-expanded')==='true')close();else open(item);}else open(item);touch=false;});
 item.addEventListener('focusout',e=>{if(!item.contains(e.relatedTarget))close();});
 });
 document.addEventListener('keydown',e=>{if(e.key==='Escape')close();});
 document.addEventListener('pointerdown',e=>{if(!group.contains(e.target))close();});
})();
