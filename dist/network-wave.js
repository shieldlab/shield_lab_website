// Original procedural network: individual nodes ease away from the pointer.
(() => {
  const banner = document.querySelector('.lab-banner');
  if (!banner) return;
  const NS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('class', 'network-wave'); svg.setAttribute('viewBox', '0 0 1200 660');
  svg.setAttribute('preserveAspectRatio', 'none'); svg.setAttribute('aria-hidden', 'true');
  const nodes = [], edges = [], cols = 22, rows = 12;
  const add = (name, attrs) => { const el = document.createElementNS(NS,name); Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));svg.append(el);return el; };
  for(let r=0;r<rows;r++) for(let c=0;c<cols;c++) {
    const u=c/(cols-1), v=r/(rows-1);
    const x=-45+u*1290 + Math.sin(r*2.1+c*1.9)*12;
    const y=330+95*Math.sin(u*5.5) + (v-.5)*830 + Math.sin(u*6+r*.6)*25;
    nodes.push({bx:x,by:y,x,y,r,c});
  }
  for(const n of nodes) {
    const i=n.r*cols+n.c;
    const links=[];
    if(n.c<cols-1)links.push(i+1);
    if(n.r<rows-1)links.push(i+cols);
    if(n.r<rows-1&&n.c<cols-1&&(n.c+n.r)%2===0)links.push(i+cols+1);
    for(const j of links)edges.push({a:n,b:nodes[j],el:add('line',{stroke:(i%4===0?'#62636a':'#70223b'),'stroke-opacity':.14+(n.c/cols)*.14,'stroke-width':.85})});
  }
  for(const [i,n] of nodes.entries())n.el=add('circle',{r:i%13===0?4.4:i%4===0?2.8:1.7,fill:i%5===0?'#666870':'#70223b','fill-opacity':.25+(n.c/cols)*.5});
  banner.prepend(svg);banner.classList.add('has-network-wave');
  const media=matchMedia('(hover: hover) and (pointer: fine) and (min-width: 801px) and (prefers-reduced-motion: no-preference)');
  const strings=document.createElementNS(NS,'svg');
  strings.setAttribute('class','icon-strings');strings.setAttribute('viewBox','0 0 1200 660');
  strings.setAttribute('preserveAspectRatio','none');strings.setAttribute('aria-hidden','true');
  const defs=document.createElementNS(NS,'defs');
  const gradient=document.createElementNS(NS,'linearGradient');
  gradient.setAttribute('id','string-fade');gradient.setAttribute('x2','100%');
  for(const [offset,opacity] of [['0%','.36'],['12%','.09'],['48%','.10'],['65%','.32'],['100%','.48']]){
    const stop=document.createElementNS(NS,'stop');stop.setAttribute('offset',offset);stop.setAttribute('stop-color','#70223b');stop.setAttribute('stop-opacity',opacity);gradient.append(stop);
  }
  defs.append(gradient);strings.append(defs);banner.prepend(strings);
  const anchors=[];
  let scaleX=1,scaleY=1;
  const bindIcons=()=>{
    const b=banner.getBoundingClientRect();scaleX=b.width/1200;scaleY=b.height/660;
    for(const a of anchors){a.icon.style.transform='';}
    for(const a of anchors){const rect=a.icon.querySelector('button').getBoundingClientRect();a.node.bx=(rect.left+rect.width/2-b.left)/scaleX;a.node.by=(rect.top+rect.height/2-b.top)/scaleY;a.node.x=a.node.bx;a.node.y=a.node.by;}
  };
  for(const icon of banner.querySelectorAll('.research-hotspot')){
    const b=banner.getBoundingClientRect(),r=icon.querySelector('button').getBoundingClientRect();
    const n={bx:(r.left+r.width/2-b.left)*1200/b.width,by:(r.top+r.height/2-b.top)*660/b.height,x:0,y:0,anchor:true};n.x=n.bx;n.y=n.by;
    const near=nodes.filter(n=>!n.anchor).sort((a,b)=>Math.hypot(a.bx-n.bx,a.by-n.by)-Math.hypot(b.bx-n.bx,b.by-n.by)).slice(0,3);
    for(const other of near)edges.push({a:n,b:other,el:add('line',{stroke:'#70223b','stroke-opacity':.28,'stroke-width':1})});
    n.el=add('circle',{r:2,fill:'#70223b'});nodes.push(n);const thread=document.createElementNS(NS,'path');thread.setAttribute('fill','none');thread.setAttribute('stroke','url(#string-fade)');thread.setAttribute('stroke-width','1.1');thread.setAttribute('vector-effect','non-scaling-stroke');strings.append(thread);anchors.push({icon,node:n,thread});
  }
  bindIcons();
  let pointer=null,frame=0,last=0;
  const render=()=>{for(const a of anchors){const x=a.node.x,y=a.node.y;a.thread.setAttribute('d',`M 14 12 Q ${14+(x-14)*.47} ${12+(y-12)*.70} ${x.toFixed(2)} ${y.toFixed(2)}`);a.icon.style.transform=media.matches?`translate(${(a.node.x-a.node.bx)*scaleX}px,${(a.node.y-a.node.by)*scaleY}px)`:'';}for(const n of nodes){n.el.setAttribute('cx',n.x.toFixed(2));n.el.setAttribute('cy',n.y.toFixed(2));}for(const e of edges){e.el.setAttribute('x1',e.a.x.toFixed(2));e.el.setAttribute('y1',e.a.y.toFixed(2));e.el.setAttribute('x2',e.b.x.toFixed(2));e.el.setAttribute('y2',e.b.y.toFixed(2));}};
  const tick=t=>{
    frame=0;const dt=Math.min(32,t-last||16);last=t;const ease=1-Math.exp(-dt/135);let moving=false;
    for(const n of nodes){let tx=n.bx,ty=n.by;if(pointer){const dx=n.bx-pointer.x,dy=n.by-pointer.y,d=Math.hypot(dx,dy),force=(n.anchor?18:38)*Math.exp(-(d*d)/(2*145*145));tx+=dx/Math.max(d,25)*force;ty+=dy/Math.max(d,25)*force;}n.x+=(tx-n.x)*ease;n.y+=(ty-n.y)*ease;if(Math.abs(tx-n.x)+Math.abs(ty-n.y)>.035)moving=true;else{n.x=tx;n.y=ty;}}
    render();if(moving)frame=requestAnimationFrame(tick);
  };
  const start=()=>{if(!frame){last=0;frame=requestAnimationFrame(tick);}};
  const reset=()=>{pointer=null;if(!media.matches||document.hidden){cancelAnimationFrame(frame);frame=0;for(const n of nodes){n.x=n.bx;n.y=n.by;}render();}else start();};
  banner.addEventListener('pointermove',e=>{if(!media.matches||e.pointerType==='touch')return;const b=banner.getBoundingClientRect();pointer={x:(e.clientX-b.left)*1200/b.width,y:(e.clientY-b.top)*660/b.height};start();},{passive:true});
  banner.addEventListener('pointerleave',reset);banner.addEventListener('pointercancel',reset);window.addEventListener('blur',reset);window.addEventListener('resize',()=>{bindIcons();reset();});media.addEventListener('change',reset);document.addEventListener('visibilitychange',reset);render();
})();
