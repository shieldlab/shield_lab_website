import json,re,html
from pathlib import Path
E=html.escape
items=json.loads(Path('data/news.json').read_text())
assert len({x['id'] for x in items})==len(items)
for x in items:
 assert re.fullmatch(r'\d{4}(?:-\d{2}(?:-\d{2})?)?',x['date'])
 for key in ('url','paperUrl','relatedUrl'):
  if x.get(key):assert x[key].startswith('https://')
 if x.get('image'):
  assert x.get('imageAlt','').strip(), 'News photos require descriptive alternative text'
  assert x['image'].startswith(('assets/','https://'))
  if x['image'].startswith('assets/'):assert (Path('dist')/x['image']).is_file()
items.sort(key=lambda x:x['date'],reverse=True)
def selected_news(entries,limit=10):
 ranked=sorted((x for x in entries if not x.get('archiveOnly')),key=lambda x:(x.get('priority',0),x['date']),reverse=True)[:limit]
 return sorted(ranked,key=lambda x:x['date'],reverse=True)
def row(x,full=False):
 date=x['date'];title=E(x['title']);url=E(x.get('url','news.html#news-'+x['id']),quote=True)
 label=E(x.get('dateLabel',date))
 heading=title if full and not x.get('url') else f'<a href="{url}">{title}<span aria-hidden="true"> ↗</span></a>'
 details=('<div class="news-details">'+''.join('<p>'+E(t)+'</p>' for t in x.get('details',[]))+'</div>') if full and x.get('details') else ''
 photo=f'<img class="news-photo" src="{E(x["image"],quote=True)}" alt="{E(x["imageAlt"],quote=True)}" width="112" height="84" loading="lazy" decoding="async">' if x.get('image') else ''
 if photo and x.get('imagePresentation')=='slide-presenter':photo='<a class="news-slide-photo" href="'+E(x['image'],quote=True)+'" aria-label="Open original panel photograph">'+photo+'</a>'
 if photo and full:photo='<div class="news-media">'+photo+'</div>'
 project=f'<a class="news-project" href="{E(x["projectUrl"],quote=True)}">{E(x.get("projectLabel","Project website"))} ↗</a>' if x.get('projectUrl') else ''
 if full and x.get('relatedUrl'):project+=f'<a class="news-project" href="{E(x["relatedUrl"],quote=True)}">{E(x["relatedLabel"])} ↗</a>'
 if full and x.get('paperUrl'):project+=f'<a class="news-project" href="{E(x["paperUrl"],quote=True)}">CVPR workshop paper ↗</a>'
 return f'<article class="news-list-item" id="news-{E(x["id"],quote=True)}" data-news-id="{E(x["id"],quote=True)}"><time datetime="{date}">{label}</time><div class="news-copy">{photo}<span class="news-category">{E(x["category"])}</span><h3>{heading}</h3><p>{E(x["summary"])}</p>{project}{details}</div></article>'
Path('dist/news-data.json').write_text(json.dumps([{k:v for k,v in x.items() if k!='directorGrant'} for x in items],ensure_ascii=False,indent=2)+'\n')
for filename,limit in [('index.html',10),('news.html',None)]:
 p=Path('dist')/filename;s=p.read_text();rows=''.join(row(x,full=limit is None) for x in (selected_news(items,limit) if limit else items))
 attrs=' tabindex="0" role="region" aria-label="Latest news, scroll for more updates"' if limit else ''
 target=f'<div{attrs} class="news-list" data-news-list="{limit or "all"}">{rows}</div>'
 if filename=='index.html':
  a=s.index('<section class="home-section" id="latest-news"');b=s.index('</section>',a)+10
  s=s[:a]+'<section class="home-section" id="latest-news"><div class="section-top"><h2>Latest News</h2><a class="text-link" href="news.html">View all news →</a></div>'+target+'</section>'+s[b:]
 else:
  a=s.index('<section class="section"');b=s.index('</section>',a)+10
  s=s[:a]+'<section class="section" aria-label="News archive">'+target+'</section>'+s[b:]
 if 'href="news-list.css"' not in s:s=s.replace('</head>','<link rel="stylesheet" href="news-list.css"></head>')
 if 'src="news-list.js"' not in s:s=s.replace('</body>','<script src="news-list.js" defer></script></body>')
 p.write_text(s)
print('News archive:',len(items),'Home:',min(10,len(items)))
# Keep director grant announcements synchronized with canonical news dates.
import subprocess,sys
subprocess.run([sys.executable,'scripts/build-director-grants.py'],check=True)
