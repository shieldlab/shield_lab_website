"""Regenerate area lists from the same built publication catalog. No bibliography copies."""
import json,re,html
from pathlib import Path
catalog=json.loads(Path('dist/publication-catalog.json').read_text())
byid={x['index']:x for x in catalog}
areas=['ai-security-privacy-forensics','llms-multimodal-agentic-ai','secure-sustainable-ai','quantum-ai-security','cyber-physical-systems']
for area in areas:
 p=Path('dist')/(area+'.html');s=p.read_text()
 selected=[x for x in catalog if area in x.get('researchAreaIds',[])]
 out='<div class="area-publication-results">'+''.join(x['html'] for x in selected)+'</div>'
 section='<section class="section area-catalog" data-research-area="'+area+'"><h2>Related Publications</h2>'+out+'</section>'
 if 'data-research-area=' in s:s=re.sub(r'<section class="section area-catalog".*?</section>',lambda m:section,s,flags=re.S)
 else:s=re.sub(r'<section class="section"><h2>Selected publications</h2><ul class="area-publications">.*?</ul></section>',lambda m:section,s,flags=re.S)
 if 'href="publications.css"' not in s:s=s.replace('</head>','<link rel="stylesheet" href="publications.css"></head>')
 if 'src="research-publications.js"' not in s:s=s.replace('</body>','<script src="research-publications.js" defer></script></body>')
 def project_ref(m):
  x=byid.get(int(m.group(1)))
  if not x:return m.group()
  title=html.escape(x['title']);url=html.escape(x.get('url') or x.get('conferenceProgramUrl') or 'publications.html#year-'+x['year'],quote=True)
  return '<span data-project-publication="'+str(x['index'])+'"><a class="text-link" href="'+url+'">'+title+' ↗</a></span>'
 s=re.sub(r'<span data-project-publication="(\d+)">.*?</span>',project_ref,s,flags=re.S)
 p.write_text(s)
 print(area,len(selected))
