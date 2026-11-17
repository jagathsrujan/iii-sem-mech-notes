#!/usr/bin/env python3
"""Build the published units for claude.ai (dist/) and GitHub Pages (docs/), then commit and push.
Usage: python3 publish.py [--no-push] [unit-id ...]   (unit ids are added to published.json first)
Only units listed in published.json (checked by the lead) go to dist/, docs/ and git."""
import json, os, re, shutil, subprocess, sys
SITE=os.path.dirname(os.path.abspath(__file__)); os.chdir(SITE)
args=[a for a in sys.argv[1:] if not a.startswith("--")]; push="--no-push" not in sys.argv
pub=json.load(open("published.json")) if os.path.exists("published.json") else []
for u in args:
    if u not in pub: pub.append(u)
order=[u["id"] for u in json.load(open("units.json"))["units"]]
pub=[u for u in order if u in pub]; json.dump(pub,open("published.json","w"),indent=1)
shutil.rmtree("dist",ignore_errors=True)
r=subprocess.run([sys.executable,"build.py",*pub],capture_output=True,text=True); print(r.stdout.strip())
if "SKIP" in r.stdout: sys.exit("a published unit failed lint or conversion; nothing pushed")
files=json.load(open("dist/files.json"))
# GitHub Pages copy: full HTML document (claude.ai wraps the page itself; Pages does not)
shutil.rmtree("docs",ignore_errors=True); shutil.copytree("dist","docs"); os.remove("docs/files.json")
src=open("dist/index.html",encoding="utf-8").read(); k=src.index("</style>")+len("</style>")
head,body=src[:k],src[k:]
reset=("<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
       "body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>")
open("docs/index.html","w",encoding="utf-8").write('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
  '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
  '<meta name="description" content="Study notes, theory answers, numericals and a study tracker for III semester B.Tech Mechanical (UVCE scheme 2026).">\n'
  +reset+"\n"+head+"\n</head>\n<body>\n"+body+"\n</body>\n</html>\n")
open("docs/.nojekyll","w").close()
# credits for every photo that ships
rows=[]
for u in pub:
    for m in json.load(open(f"manifest/{u}.json")):
        rows.append(f"| `{m['file']}` | {m.get('caption','').replace('|','/')} | {m.get('author','').replace('|','/')} | {m.get('license','')} | [source]({m.get('commons_page','')}) |")
open("CREDITS.md","w",encoding="utf-8").write("# Photo credits\n\nAll photos come from Wikimedia Commons under the licences below. They keep their own licences.\n\n"
  "| File | Shows | Author | Licence | Source |\n|---|---|---|---|---|\n"+"\n".join(rows)+"\n")
# stage only public-safe paths
paths=["README.md","CREDITS.md",".gitignore","published.json","units.json","NOTES_SPEC.md","index.src.html","lint.py","build.py","preview.py","publish.py",
       "tools/tex2svg.js","tools/package.json","tools/package-lock.json","docs"]
paths+= [f"content/{u}.html" for u in pub]+[f"manifest/{u}.json" for u in pub]+[f for f in files if f.startswith("img/")]
subprocess.run(["git","add","--",*[p for p in paths if os.path.exists(p)]],check=True)
st=subprocess.run(["git","diff","--cached","--name-only"],capture_output=True,text=True).stdout.split()
if st:
    subprocess.run(["git","commit","-q","-m",f"Publish {len(pub)} units: {', '.join(pub)}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"],check=True)
    if push: subprocess.run(["git","push","-q","origin","main"],check=True)
print(f"published units: {len(pub)} | staged changes: {len(st)} | pushed: {bool(st) and push}")
print("ARTIFACT_FILES="+json.dumps(files))
