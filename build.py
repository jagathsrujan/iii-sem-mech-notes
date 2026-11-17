#!/usr/bin/env python3
"""Build dist/: index.html with units injected, plus content/ and img/ for the units given (or all that pass lint)."""
import json, os, re, shutil, subprocess, sys
SITE=os.path.dirname(os.path.abspath(__file__)); DIST=os.path.join(SITE,"dist")
TEX2SVG=os.path.join(SITE,"tools","tex2svg.js")
units=json.load(open(os.path.join(SITE,"units.json")))
slim={"subjects":units["subjects"],"units":[{k:u[k] for k in ("id","subject","n","title","due","targets")} for u in units["units"]]}
src=open(os.path.join(SITE,"index.src.html"),encoding="utf-8").read()
assert "/*UNITS*/null" in src
os.makedirs(os.path.join(DIST,"content"),exist_ok=True); os.makedirs(os.path.join(DIST,"img"),exist_ok=True)
open(os.path.join(DIST,"index.html"),"w",encoding="utf-8").write(src.replace("/*UNITS*/null",json.dumps(slim,separators=(",",":"))))
want=sys.argv[1:] or [u["id"] for u in units["units"]]
files=[]
for uid in want:
    f=os.path.join(SITE,"content",uid+".html")
    if not os.path.exists(f): continue
    r=subprocess.run([sys.executable,os.path.join(SITE,"lint.py"),uid],capture_output=True,text=True)
    if "RESULT: PASS" not in r.stdout: print(f"SKIP {uid}: lint fails"); continue
    html=open(f,encoding="utf-8").read()
    t=subprocess.run(["node",TEX2SVG,f,os.path.join(DIST,"content",uid+".html")],capture_output=True,text=True)
    print("     ",t.stdout.strip().replace("\n","\n      "))
    if t.returncode!=0: print(f"SKIP {uid}: formula conversion failed"); os.remove(os.path.join(DIST,"content",uid+".html")); continue
    files.append(f"content/{uid}.html")
    for src_img in sorted(set(re.findall(r'src="(img/[^"]+)"',html))):
        shutil.copy(os.path.join(SITE,src_img),os.path.join(DIST,src_img)); files.append(src_img)
    print(f"OK   {uid}")
json.dump(files,open(os.path.join(DIST,"files.json"),"w"),indent=0)
print(len(files),"files;", "index", os.path.getsize(os.path.join(DIST,"index.html"))//1024,"KB")
