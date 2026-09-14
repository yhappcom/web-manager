#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from xml.sax.saxutils import escape

BASE='https://minttap.app'
PAGES=[
 ('ko/','ko','MintTap','MintTap 앱과 지원 정보를 확인합니다.'),
 ('en/','en','MintTap','MintTap apps and support information.'),
 ('ko/apps/example/','ko','Example App','POC용 합성 앱 페이지입니다.'),
 ('en/apps/example/','en','Example App','Synthetic app page for provider POC.'),
 ('ko/apps/example/support/','ko','지원','POC용 합성 지원 페이지입니다.'),
 ('en/apps/example/support/','en','Support','Synthetic support page for provider POC.'),
 ('ko/apps/example/privacy/','ko','개인정보 처리방침','POC용 합성 개인정보 페이지이며 실제 정책이 아닙니다.'),
 ('en/apps/example/privacy/','en','Privacy','Synthetic privacy page for provider POC; not a real policy.'),
]

def page(path,lang,title,body):
    canonical=f'{BASE}/{path}'
    alt='en' if lang=='ko' else 'ko'
    alt_path=path.replace('ko/','en/',1) if lang=='ko' else path.replace('en/','ko/',1)
    return f'''<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{escape(title)}</title>\n<link rel="canonical" href="{canonical}">\n<link rel="alternate" hreflang="{lang}" href="{canonical}">\n<link rel="alternate" hreflang="{alt}" href="{BASE}/{alt_path}">\n</head>\n<body><main><h1>{escape(title)}</h1><p>{escape(body)}</p></main></body>\n</html>\n'''

def sha256_bytes(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def verify(out:Path, manifest_path:Path):
    m=json.loads(manifest_path.read_text(encoding='utf-8'))
    observed=[]
    for item in m['files']:
        p=out/item['path']
        if not p.is_file(): return False, f"missing:{item['path']}"
        data=p.read_bytes(); digest=sha256_bytes(data)
        if digest!=item['sha256'] or len(data)!=item['bytes']: return False, f"changed:{item['path']}"
        observed.append({'path':item['path'],'sha256':digest,'bytes':len(data)})
    aggregate=''.join(f"{x['path']}\0{x['sha256']}\n" for x in observed).encode()
    digest='sha256:'+sha256_bytes(aggregate)
    return (digest==m['artifact_digest'], None if digest==m['artifact_digest'] else 'aggregate-digest-mismatch')

def build(out:Path, manifest_path:Path):
    out.mkdir(parents=True, exist_ok=True)
    for path,lang,title,body in PAGES:
        p=out/path/'index.html'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(page(path,lang,title,body),encoding='utf-8')
    (out/'404.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>Not Found</title></head><body><main><h1>404</h1><p>Page not found.</p></main></body></html>\n',encoding='utf-8')
    wk=out/'.well-known'; wk.mkdir(exist_ok=True)
    aasa={"applinks":{"details":[{"appIDs":["TEAMID.com.example.synthetic"],"components":[{"/":"/open/*"}]}]}}
    (wk/'apple-app-site-association').write_text(json.dumps(aasa,separators=(',',':'))+'\n',encoding='utf-8')
    asset=[{"relation":["delegate_permission/common.handle_all_urls"],"target":{"namespace":"android_app","package_name":"com.example.synthetic","sha256_cert_fingerprints":["00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF"]}}]
    (wk/'assetlinks.json').write_text(json.dumps(asset,separators=(',',':'))+'\n',encoding='utf-8')
    (out/'app-ads.txt').write_text('# Synthetic POC placeholder. Replace only when real advertising facts exist.\n',encoding='utf-8')
    (out/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n',encoding='utf-8')
    urls=''.join(f'<url><loc>{BASE}/{escape(path)}</loc></url>' for path,_,_,_ in PAGES)
    (out/'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',encoding='utf-8')
    files=[]
    for p in sorted(x for x in out.rglob('*') if x.is_file()):
        rel=p.relative_to(out).as_posix(); data=p.read_bytes(); files.append({'path':rel,'sha256':sha256_bytes(data),'bytes':len(data)})
    aggregate=''.join(f"{x['path']}\0{x['sha256']}\n" for x in files).encode()
    manifest={'schema':'minttap-poc-artifact-v1','base_url':BASE,'synthetic':True,'file_count':len(files),'artifact_digest':'sha256:'+sha256_bytes(aggregate),'files':files}
    manifest_path.parent.mkdir(parents=True,exist_ok=True); manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return manifest

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); ap.add_argument('--manifest',required=True); ap.add_argument('--verify',action='store_true'); args=ap.parse_args()
    if args.verify:
        ok,reason=verify(Path(args.output),Path(args.manifest)); print(json.dumps({'ok':ok,'reason':reason},indent=2)); raise SystemExit(0 if ok else 1)
    m=build(Path(args.output),Path(args.manifest)); print(json.dumps({'artifact_digest':m['artifact_digest'],'file_count':m['file_count']},indent=2))
if __name__=='__main__': main()
