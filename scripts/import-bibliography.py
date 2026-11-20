import csv,json,re,html
from pathlib import Path
from collections import defaultdict
rows=list(csv.DictReader(open('data/citations.csv',encoding='utf-8-sig')))
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
verified={norm(x['title']):x for x in json.load(open('data/verified-publications.json'))}
links={}
for f in ['data/pub-links-early.json','data/pub-links-recent.json']:
 if Path(f).exists():links.update(json.load(open(f)))
# Coalesce duplicate exports and published/preprint variants; keep all distinct works.
skip={31,32,48,56,58,61,79,80,81,82,83,85,89}
merge={22:[56],29:[32],30:[31],45:[48],57:[58],60:[61],73:[81,83],76:[80],77:[79],78:[82],84:[85],88:[89]}
items=[]
for i,r0 in enumerate(rows):
 if i in skip:continue
 r=dict(r0); title=r['Title']; note=[]; link=''; typ=''; year=r['Year'];v=verified.get(norm(title)); m=links.get(str(i),{})
 if v:
  link=v['url'];year=str(v['year']);typ=v['type'].title();r['Publication']=v['venue'];r['Authors']='; '.join(v['authors']);
  if v.get('note'):note.append(v['note'])
 if m.get('url'):link=m['url']
 if m.get('type') and m['type']!='unresolved':typ=m['type'].title()
 if m.get('year'):year=str(m['year'])
 if i==24:note.append('2024 issue publication; the supplied bibliography lists 2023 early access.')
 for k in ['Title','Publication','Pages','Volume','Number','Authors']:
  if m.get(k.lower()):r[k]=m[k.lower()]
 venue=r['Publication']; low=(venue+' '+title+' '+r['Publisher']).lower()
 # Explicit record-type labels prevent posters and preprints becoming full articles.
 if 'poster' in title.lower() or 'panel' in title.lower():typ='Poster / abstract' if 'poster' in title.lower() else 'Panel'
 elif 'arxiv' in venue.lower() or 'techrxiv' in low:typ='Preprint' if not ('conference' in venue.lower() and 'accepted' in venue.lower()) else 'Conference'
 elif i==12:typ='Dissertation'
 elif not typ:
  if 'workshop' in low:typ='Workshop'
  elif 'symposium series' in low:typ='Symposium'
  elif any(x in low for x in ['journal','transactions','magazine','axioms','ai & society']):typ='Journal'
  elif 'blockchains' in venue.lower():typ='Book chapter'
  elif venue:typ='Conference'
  else:typ='Record'
 if i==42:r['Publication']='2024 IEEE 44th International Conference on Distributed Computing Systems Workshops (ICDCSW)'
 if i==9:typ='Demo'
 if i==57:typ='Conference';r['Publication']=r0['Publication']
 if i==55:typ='Workshop';r['Publication']=r0['Publication']
 if i==73:typ='Workshop';r['Publication']='IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshop';r['Pages']=rows[81]['Pages']
 if i==22:year='2023';typ='Book chapter';link='https://doi.org/10.1007/978-3-031-10507-4_5';note=['Publisher citation year used; Scholar export contains conflicting 2012/2022 dates.']
 if i==68:typ='Preprint';r['Publication']='TechRxiv'
 if i==86:r['Authors']='Mohd. Farhan Israk Soumik; Awal Ahmed Fime; Malithi Mithsara Wanniarachchi Kankanamge; Arun Babu Aryal; Hoda Joudi Haghighi; Bibek Koirala; Ahmed Imteaj; Abdur R. Shahid';r['Pages']='37756–37789'
 if i==75:r['Pages']='1866–1885'
 if not link:
  ar=re.search(r'(\d{4}\.\d{4,5})',r0['Publication']+' '+r0['Pages'])
  if ar:link='https://arxiv.org/abs/'+ar.group(1)
 if not r['Publication']:note.append('Venue details are incomplete in the supplied bibliography.')
 if not year:note.append('Publication year not supplied.')
 authors=[]
 for a in r['Authors'].split(';'):
  a=a.strip()
  if not a:continue
  if ', ' in a:last,first=a.split(', ',1);a=first+' '+last
  authors.append(a)
 items.append(dict(index=i,title=r['Title'],authors=authors,venue=r['Publication'],year=year,type=typ,url=link,volume=r['Volume'],number=r['Number'],pages=r['Pages'],publisher=r['Publisher'],doi=m.get('doi',''),pdf=m.get('pdf',''),abstract=m.get('abstract',''),note=' '.join(dict.fromkeys(note))))
items=[x for x in items if x['year']!='2012']
items.sort(key=lambda x:(-int(x['year'] or 0),x['title'].lower()))
Path('data/publications.json').write_text(json.dumps(items,indent=2,ensure_ascii=False))
