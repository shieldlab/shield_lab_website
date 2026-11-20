(async()=>{
 const targets=[...document.querySelectorAll('[data-publication-catalog]')];if(!targets.length)return;
 try{
 const response=await fetch('publication-catalog.json',{cache:'no-cache'});if(!response.ok)throw Error('Catalog unavailable');const records=await response.json();
 for(const target of targets){const id=target.dataset.publicationCatalog,selected=records.filter(p=>id==='all'||p.memberIds.includes(id));const groups=new Map;selected.forEach(p=>{if(!groups.has(p.year))groups.set(p.year,[]);groups.get(p.year).push(p)});
 if(id==='all'){
 target.querySelectorAll('section[id^="year-"]').forEach(e=>e.remove());
 for(const [year,papers]of groups){const section=document.createElement('section');section.className='section';section.id='year-'+year;section.innerHTML='<div class="pub-year-heading"><h2>'+year+'</h2><span>'+papers.length+' publications</span></div>'+papers.map(p=>p.html).join('');target.append(section)}
 const nav=target.querySelector('.publication-years');nav.replaceChildren();for(const year of groups.keys()){const a=document.createElement('a');a.href='#year-'+year;a.textContent=year;nav.append(a)}
 }else{
 const output=target.querySelector('.member-publication-results');target.hidden=!selected.length;output.innerHTML=selected.map(p=>p.html).join('');target.dataset.publicationCount=selected.length;
 }
 }
 document.dispatchEvent(new Event('publication-catalog-ready'));
 }catch(error){for(const target of targets){if(target.dataset.publicationCatalog!=='all')target.querySelector('.member-publication-results').innerHTML='<p>Publications are temporarily unavailable. <a href="publications.html">View the lab bibliography</a>.</p>'}document.dispatchEvent(new Event('publication-catalog-ready'))}
})();
