import json,re,html
from pathlib import Path
from profile_links import profile_links
E=html.escape
members=json.loads(Path('data/members.json').read_text())
template=Path('dist/team.html').read_text();head=template[:template.index('<main')];tail=template[template.index('</main>')+7:]
head=head.replace('<title>Team |','<title>PROFILE |').replace('aria-current="page"','')
head=head.replace('</head>','<link rel="stylesheet" href="publications.css"><link rel="stylesheet" href="profiles.css"><link rel="stylesheet" href="profile-links.css"></head>')
for m in members[1:]:
 portrait=f'<img src="assets/{m["image"]}" alt="{E(m["name"])}">' if m.get('image') else f'<div class="profile-placeholder" role="img" aria-label="Portrait unavailable for {E(m["name"])}">{m["initials"]}</div>'
 links=profile_links(m)

 edu='<h2>Education</h2><ul>'+''.join('<li>'+E(x)+'</li>' for x in m['education'])+'</ul>' if m.get('education') else ''
 extra=('<h2>Professional Experience</h2><p>'+E(m['experience'])+'</p>' if m.get('experience') else '')
 extra+=('<h2>Teaching</h2><p>'+E(m['teaching'])+'</p>' if m.get('teaching') else '')
 certifications=('<h2>Certifications</h2><ul>'+''.join('<li>'+E(x)+'</li>' for x in m['certifications'])+'</ul>' if m.get('certifications') else '')

 certifications+=('<h2>Technical Skills</h2><ul>'+''.join('<li>'+E(x)+'</li>' for x in m['skills'])+'</ul>' if m.get('skills') else '')
 certifications+=('<h2>Awards & Service</h2><ul>'+''.join('<li>'+E(x)+'</li>' for x in m['awards'])+'</ul>' if m.get('awards') else '')
 interests='<h2>Research Interests</h2><p>'+E(m['interests'])+'</p>' if m.get('interests') else ''
 body=f'<main class="member-page"><section class="section member-hero"><div>{portrait}</div><div><a class="text-link" href="team.html">← Team</a><h1>{E(m["name"])}</h1><p class="member-role">{E(m["role"])}</p><p>SHIELD Lab · Southern Illinois University Carbondale</p><div class="profile-socials">{links}</div></div></section><section class="section member-biography"><div><h2>About</h2><p>{E(m["bio"])}</p>{edu}{extra}</div><aside>{interests}{certifications}</aside></section><section class="section member-publications" data-publication-catalog="{m["id"]}"><h2>Publications</h2><div class="member-publication-results"><p>Loading publications…</p></div><noscript><p><a href="publications.html">Browse all lab publications</a>.</p></noscript></section></main>'
 Path('dist/member-'+m['id']+'.html').write_text(head.replace('PROFILE',E(m['name']))+body+tail.replace('</body>','<script src="publication-catalog.js" defer></script></body>'))
# Existing cards retain external personal links and add clear local profiles.
s=template
for m in members[1:]:
 old='<h3>'+m['name']+'</h3>';s=s.replace(old,'<h3><a href="member-'+m['id']+'.html">'+m['name']+'</a></h3>')
Path('dist/team.html').write_text(s)
# Director shares the same optional, owner-supplied social-link configuration.
p=Path('dist/director.html');s=p.read_text();m=members[0]
links=profile_links(m)
block='<div class="actions profile-socials" data-profile-links="director"'+('' if links else ' hidden')+'>'+links+'</div>'
if 'data-profile-links="director"' in s:s=re.sub(r'<div class="actions(?: profile-socials)?" data-profile-links="director"[^>]*>.*?</div>',block,s)
else:s=s.replace('<section class="section bio-grid">',block+'<section class="section bio-grid">')
if 'href="profile-links.css"' not in s:s=s.replace('</head>','<link rel="stylesheet" href="profile-links.css"></head>')
p.write_text(s)
