#!/usr/bin/env python3
"""Render a unit the way the student sees it (formulas converted, app CSS) to PNG pages.
Usage: python3 preview.py <unit-id> [--width 900]  ->  _work/<unit-id>/preview/page-NN.png
Look at the PNGs with the Read tool. Never open the browser pane."""
import os, re, subprocess, sys, tempfile
SITE=os.path.dirname(os.path.abspath(__file__))
TEX2SVG=os.path.join(SITE,"tools","tex2svg.js")
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
uid=sys.argv[1]; width=int(sys.argv[sys.argv.index("--width")+1]) if "--width" in sys.argv else 900
out=os.path.join(SITE,"_work",uid,"preview"); os.makedirs(out,exist_ok=True)
for f in os.listdir(out): os.remove(os.path.join(out,f))
conv=os.path.join(out,"_frag.html")
r=subprocess.run(["node",TEX2SVG,os.path.join(SITE,"content",uid+".html"),conv],capture_output=True,text=True)
print(r.stdout.strip())
src=open(os.path.join(SITE,"index.src.html"),encoding="utf-8").read()
css=re.search(r"<style>(.*?)</style>",src,re.S).group(1)
hatch=re.search(r'(<svg width="0" height="0" aria-hidden="true" focusable="false" class="hatchdefs".*?</svg>)',src,re.S).group(1)
frag=open(conv,encoding="utf-8").read().replace('src="img/',f'src="file://{SITE}/img/')
extra="dl.cards{display:block}dl.cards dt{font-weight:700;margin-top:8px}.mcq .why{display:block}body{padding:20px}@page{size:%dpx 1400px;margin:0}"%width
page=f'<!doctype html><html><head><meta charset="utf-8"><style>{css}{extra}</style></head><body>{hatch}<div style="max-width:{width-40}px">{frag}</div></body></html>'
ph=os.path.join(out,"_preview.html"); open(ph,"w",encoding="utf-8").write(page)
pdf=os.path.join(out,"_preview.pdf")
subprocess.run([CHROME,"--headless=new","--disable-gpu","--no-pdf-header-footer","--allow-file-access-from-files",f"--print-to-pdf={pdf}","--virtual-time-budget=4000","file://"+ph],capture_output=True,timeout=120)
import pymupdf
d=pymupdf.open(pdf)
for i,p in enumerate(d): p.get_pixmap(dpi=80).save(os.path.join(out,f"page-{i+1:02d}.png"))
print(f"{d.page_count} pages -> {out}/page-NN.png")
