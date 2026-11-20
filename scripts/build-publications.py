import json,re,html
from pathlib import Path
from collections import defaultdict
from publication_topic_chart import render_topic_chart
items=json.loads(Path("data/publications.json").read_text())
area_ids=set(json.loads(Path('data/research-area-taxonomy.json').read_text()))
for record in items:
 assigned=record.get('researchAreaIds',[])
 assert isinstance(assigned,list) and len(assigned)==len(set(assigned))
 assert set(assigned)<=area_ids, 'Unknown research area ID'
items.sort(key=lambda x:(-int(x["year"] or 0),x["title"].lower()))
e=html.escape
rankings=json.load(open("data/venue-rankings.json"))
topicdata=json.load(open("data/publication-topics.json"))
def article(x):
 typ=x['type'];css=re.sub('[^a-z-]','',typ.lower().replace(' ','-'))
 details=[]
 if x['volume']:details.append('vol. '+x['volume'])
 if x['number']:details.append('no. '+x['number'])
 if x['pages']:details.append('pp. '+x['pages'])
 if x['year']:details.append(x['year'])
 citation=e(x['venue'] or x['publisher'] or '')
 if details:citation+=(' · ' if citation else '')+e(', '.join(details))
 note=''
 actions=[]
 if x.get("conferenceProgramUrl"):actions.append('<a class="pub-action" href="'+e(x["conferenceProgramUrl"],quote=True)+'">Conference program ↗</a>')
 if x['abstract']:actions.append('<details class="pub-disclosure"><summary>Summary</summary><div class="pub-abstract">'+e(x['abstract'])+'</div></details>')
 if x['pdf']:actions.append(f'<a class="pub-action pdf" href="{e(x["pdf"],quote=True)}">PDF</a>')
 if x['url']:actions.append(f'<a class="pub-action paper" href="{e(x["url"],quote=True)}">Paper ↗</a>')
 doi=x['doi'] or (x['url'].split('doi.org/',1)[1] if 'doi.org/' in x['url'] else '')
 if doi:actions.append(f'<a class="pub-action doi" href="https://doi.org/{e(doi,quote=True)}">DOI ↗</a>')
 bt={'Journal':'article','Conference':'inproceedings','Workshop':'inproceedings','Symposium':'inproceedings','Book chapter':'incollection','Dissertation':'phdthesis'}.get(typ,'misc')
 fields={'title':x['title'],'author':' and '.join(x['authors']),'year':x['year']}
 if x['venue']:fields['journal' if bt=='article' else 'booktitle' if bt in ['inproceedings','incollection'] else 'howpublished']=x['venue']
 for k in ['volume','number','pages','publisher']:
  if x[k]:fields[k]=x[k]
 if doi:fields['doi']=doi
 if x['url']:fields['url']=x['url']
 bib='@'+bt+'{shield'+str(x['index'])+',\n'+',\n'.join('  '+k+' = {'+v.replace('{','').replace('}','')+'}' for k,v in fields.items() if v)+'\n}'
 actions.append('<details class="pub-disclosure bibtex"><summary>BibTeX</summary><pre>'+e(bib)+'</pre></details>')
 pending=''
 topics=topicdata['assignments'].get(str(x['index']),[])
 topicmarkup='<div class="pub-topics" aria-label="Research topics">'+(''.join('<span>'+e(t)+'</span>' for t in topics) if topics else '<span class="untagged">Topic not assigned</span>')+'</div>'
 rank=rankings.get(str(x['index']))
 badge=(f'<a class="venue-rank" href="{rank["source"]}" title="Conference venue rating, not an individual paper assessment">ICORE {rank["rank"]}<small>2026 edition</small></a>' if rank else '')
 metrics={72:('4.9','https://www.nature.com/srep/about'),38:('6.1','https://link.springer.com/journal/146'),0:('1.5','https://www.mdpi.com/journal/axioms/imprint')}
 if x['index'] in metrics:
  value,source=metrics[x['index']];badge+=f'<a class="venue-rank" href="{source}">JIF {value}<small>2025 metric</small></a>'
 if x['index'] in [63,73]:badge+='<span class="venue-highlight">CVPR Workshop</span>'
 if x['index']==21:badge+='<span class="venue-highlight">IEEE TrustCom</span>'
 if x['index']==3:badge+='<span class="venue-highlight">TrustCom / BigDataSE</span>'
 if x['index']==39:badge+='<span class="venue-highlight">IEEE ICC Workshop</span>'
 if x['index']==57:badge+='<span class="venue-highlight">IEEE GLOBECOM</span>'
 if x['index']==36:badge+='<span class="venue-highlight">INFOCOM Poster</span>'
 if x['index']==54:badge+='<span class="venue-highlight">NeurIPS Workshop · Poster</span>'
 if x['venue']=='IEEE Transactions on Sustainable Computing':badge+='<a class="venue-rank" href="https://open.ieee.org/wp-content/uploads/IEEE-Title-List-September-2026-CAPES.pdf">JIF 5.3<small>2025 metric</small></a>'
 if x['venue']=='IEEE Consumer Electronics Magazine':badge+='<a class="venue-rank" href="https://open.ieee.org/wp-content/uploads/IEEE-Title-List-August-2026.pdf">JIF 5.0<small>2025 metric</small></a>'

 return f'<article class="publication" data-type="{e(typ)}" data-topics="{e(json.dumps(topics),quote=True)}">{badge}<span class="tag type-{css}">{e(typ)}</span><h3>{e(x["title"])}</h3><p class="pub-authors">{e(", ".join(x["authors"]))}</p><p class="pub-venue"><strong>{citation}</strong></p>{topicmarkup}<div class="pub-actions">'+''.join(actions)+'</div>'+note+pending+'</article>'
groups=defaultdict(list)
for x in items:groups[x['year'] or 'Year not supplied'].append(x)
nav='<nav class="publication-years" aria-label="Publication years">'+''.join(f'<a href="#year-{e(y)}">{e(y)}</a>' for y in groups if y.isdigit())+'</nav>'
filters='<div class="publication-filters"><div><label for="topic-filter">Research topic</label><select id="topic-filter"><option value="">All topics</option>'+''.join('<option>'+e(t)+'</option>' for t in topicdata['taxonomy'])+'<option value="untagged">Topic not assigned</option></select></div><div><label for="publication-search">Search publications</label><input id="publication-search" type="search" placeholder="Title, author or venue"></div><button type="button" id="reset-publications">Reset filters</button></div><p class="filter-status" id="filter-status" role="status" aria-live="polite">Showing all '+str(len(items))+' publications</p><noscript><p>Filtering requires JavaScript. All publications remain available below.</p></noscript>'
body=f'<section class="page-intro"><h1>Publications</h1>{filters}{nav}</section><p id="no-publications" hidden>No publications match these filters. Try another topic or reset filters.</p>'
body+=render_topic_chart(items, topicdata)
for year,g in groups.items():body+=f'<section class="section" id="year-{e(year)}"><div class="pub-year-heading"><h2>{e(year)}</h2><span>{len(g)} publications</span></div>'+''.join(article(x) for x in g)+'</section>'
p=Path('dist/publications.html');s=p.read_text();start=s.index('<main');end=s.index('</main>',start);s=s.replace('</head>','<link rel="stylesheet" href="publications.css"></head>') if 'publications.css' not in s else s;s=s[:s.index('<main')]+ '<main class="publications-page">'+body+s[s.index('</main>'):];s=s.replace('</body>','<script src="publication-filters.js" defer></script></body>') if 'publication-filters.js' not in s else s;p.write_text(s)

# One catalog drives the full bibliography and every member publication list.
identities=json.loads(Path('data/members.json').read_text())
def normalize(a):return re.sub(r'[^a-z0-9]','',a.casefold())
for x in items:
 x['memberIds']=[m['id'] for m in identities if any(normalize(a) in {normalize(v) for v in m.get('authorAliases',[])} for a in x['authors']) or x['index'] in m.get('verifiedPublicationIds',[])]
 x['html']=article(x)
Path('dist/publication-catalog.json').write_text(json.dumps(items,ensure_ascii=False))
s=Path('dist/publications.html').read_text().replace('<main class="publications-page">','<main class="publications-page" data-publication-catalog="all">')
s=re.sub(r'<script src="publication-catalog.js" defer></script>','',s)
s=s.replace('<script src="publication-filters.js" defer></script>','<script src="publication-catalog.js" defer></script><script src="publication-filters.js" defer></script>')
Path('dist/publications.html').write_text(s)
print('Published shared catalog:',len(items),'publications')
# Rebuild research-area fallbacks after the shared catalog, without touching profile markup.
import subprocess,sys
subprocess.run([sys.executable,'scripts/build-area-publications.py'],check=True)
