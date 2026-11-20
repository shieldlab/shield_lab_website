(async()=>{
 const targets=[...document.querySelectorAll('[data-research-area]')];if(!targets.length)return;
 try{const response=await fetch('publication-catalog.json',{cache:'no-cache'});if(!response.ok)return;
 const records=await response.json();
 for(const ref of document.querySelectorAll('[data-project-publication]')){const paper=records.find(p=>String(p.index)===ref.dataset.projectPublication);if(!paper)continue;const a=document.createElement('a');a.className='text-link';a.href=paper.url||paper.conferenceProgramUrl||'publications.html#year-'+paper.year;a.textContent=paper.title+' ↗';ref.replaceChildren(a);}
 for(const target of targets){const selected=records.filter(p=>(p.researchAreaIds||[]).includes(target.dataset.researchArea));
 target.querySelector('.area-publication-results').innerHTML=selected.length?selected.map(p=>p.html).join(''):'<p>No publications are currently assigned to this research area.</p>';
 target.dataset.publicationCount=selected.length;}
 }catch{ /* Generated canonical-catalog fallback remains visible. */ }
})();
