from html import escape
from urllib.parse import urlparse
ICONS={
'linkedin':('LinkedIn','<rect x="3" y="8" width="4" height="13"/><circle cx="5" cy="4" r="2"/><path d="M11 21V8h4v2c3-4 7-2 7 2v9h-4v-8c0-3-3-3-3 0v8z"/>'),
'scholar':('Google Scholar','<path d="M1 9 12 2l11 7-11 7z"/><path d="M5 13v5c4 4 10 4 14 0v-5" fill="none" stroke="currentColor" stroke-width="2"/>'),
'website':('Personal website','<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7"/><ellipse cx="12" cy="12" rx="4" ry="9" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M3 12h18M5 7h14M5 17h14" fill="none" stroke="currentColor" stroke-width="1.5"/>'),
'github':('GitHub','<path d="M12 2a10 10 0 0 0-3 19.5v-2.7c-2.5.5-3-1-3-1-.4-1-1-1.3-1-1.3-.8-.5.1-.5.1-.5.9.1 1.4.9 1.4.9.8 1.3 2 1 2.6.8.1-.6.4-1 .7-1.2-2-.2-4-1-4-4.5 0-1 .4-1.8 1-2.5-.1-.3-.4-1.3.1-2.6 0 0 .8-.3 2.8 1a10 10 0 0 1 5.2 0c2-1.3 2.8-1 2.8-1 .5 1.3.2 2.3.1 2.6.6.7 1 1.5 1 2.5 0 3.5-2.1 4.3-4.1 4.5.4.3.7.9.7 1.7v3.3A10 10 0 0 0 12 2z"/>')}
def valid_url(value):
 try:
  p=urlparse(value)
  return p.scheme=='https' and bool(p.hostname) and '.' in p.hostname and not p.username and not p.password and not any(c.isspace() for c in value)
 except (ValueError,TypeError):return False
def profile_links(member):
 links=[]
 for key,(label,paths) in ICONS.items():
  label=member.get('profileLinkLabels',{}).get(key,label)
  url=member.get('profileLinks',{}).get(key,'')
  if valid_url(url):links.append(f'<a class="profile-social" href="{escape(url,quote=True)}" aria-label="{escape(member["name"])} — {label}" title="{label}"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor">{paths}</svg><span>{label}</span></a>')
 return ''.join(links)
