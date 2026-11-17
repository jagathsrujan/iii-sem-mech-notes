#!/usr/bin/env python3
"""Lint one unit fragment against NOTES_SPEC.md.  Usage: python3 lint.py <unit-id> [<unit-id> ...]"""
import json, os, re, sys
from html.parser import HTMLParser

SITE = os.path.dirname(os.path.abspath(__file__))
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","source","track","wbr"}
SVG_VOID_OK = {"path","line","rect","circle","ellipse","polyline","polygon","stop","use"}  # may self-close
BANNED = {"script","style","link","iframe","object","embed","html","head","body","meta","base","form"}
SVG_CLASSES = {"ln","thin","thick","dash","hid","acc","acc2","fill-soft","fill-acc","fill-acc2","fill-hatch","solid",
               "lbl","lbl-sm","lbl-b","lbl-acc"}
COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(|\b(red|blue|green|black|white|gray|grey|orange|yellow|purple)\b")
WIDGETS = {"taper-bar","stress-strain","beam-ss","torsion","mohr","carnot","vcr","unit-cells","lever-rule","merchant"}

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.stack=[]; s.errors=[]; s.warns=[]; s.ids=[]; s.in_svg=0; s.imgs=[]; s.widgets=[]
        s.parts=[]; s.qsrc=[]; s.text_by_part={}; s.cur_part=None; s.part_depth=None; s.counts={}
        s.in_qsrc=False; s.svg_count=0; s.mcq=0; s.cards=0
    def cnt(s,k): s.counts[k]=s.counts.get(k,0)+1
    def handle_starttag(s,tag,attrs):
        a=dict(attrs); line=s.getpos()[0]
        if tag in BANNED: s.errors.append(f"L{line}: banned tag <{tag}>")
        for k,v in attrs:
            if k.startswith("on"): s.errors.append(f"L{line}: event attribute {k}")
            if k=="style": s.errors.append(f"L{line}: style= attribute not allowed")
        if "id" in a: s.ids.append((a["id"],line))
        cls=(a.get("class") or "").split()
        if tag=="svg": s.in_svg+=1; s.svg_count+=1
        if s.in_svg:
            for k in ("fill","stroke","stop-color","color"):
                v=a.get(k)
                if v and v not in ("none","currentColor") and not v.startswith("url(#"):
                    s.errors.append(f"L{line}: literal colour {k}=\"{v}\" in SVG")
            for c in cls:
                if c not in SVG_CLASSES: s.warns.append(f"L{line}: unknown SVG class '{c}'")
        if tag=="img":
            s.imgs.append((a.get("src",""),line))
            for k in ("alt","width","height"):
                if k not in a: s.errors.append(f"L{line}: <img> missing {k}")
        if "widget" in cls and tag=="div": s.widgets.append((a.get("data-widget"),line))
        if tag=="section" and "part" in cls:
            s.parts.append((a.get("id"),a.get("data-part"))); s.cur_part=a.get("data-part"); s.part_depth=len(s.stack)
        if "q-src" in cls: s.in_qsrc=True; s.qsrc.append("")
        if "mcq" in cls:
            s.mcq+=1
            if a.get("data-answer") not in list("abcd"): s.errors.append(f"L{line}: .mcq data-answer must be a-d")
        for c in ("q","num","fig","photo","formula","answer"):
            if c in cls: s.cnt(c+(".practice" if c=="num" and "practice" in cls else ""))
        if tag=="dt" : s.cards+=1
        if tag not in VOID and not (s.in_svg and tag in SVG_VOID_OK and s._selfclose):
            s.stack.append((tag,line))
    def handle_startendtag(s,tag,attrs):
        s._selfclose=True; s.handle_starttag(tag,attrs); s._selfclose=False
        if tag=="svg": s.in_svg-=1
    _selfclose=False
    def handle_endtag(s,tag):
        line=s.getpos()[0]
        if tag in VOID: return
        if not s.stack: s.errors.append(f"L{line}: stray </{tag}>"); return
        if s.stack[-1][0]==tag:
            s.stack.pop()
        else:
            names=[t for t,_ in s.stack]
            if tag in names:
                while s.stack and s.stack[-1][0]!=tag:
                    t,l=s.stack.pop(); s.errors.append(f"L{l}: <{t}> not closed before </{tag}> at L{line}")
                s.stack.pop()
            else: s.errors.append(f"L{line}: stray </{tag}>")
        if tag=="svg": s.in_svg-=1
        if s.in_qsrc and tag=="p": s.in_qsrc=False
        if s.part_depth is not None and len(s.stack)==s.part_depth: s.cur_part=None; s.part_depth=None
    def handle_data(s,d):
        if s.in_svg:
            if COLOR_RE.search(d) and "<" not in d: pass
            return
        if s.in_qsrc: s.qsrc[-1]+=d
        if s.cur_part: s.text_by_part[s.cur_part]=s.text_by_part.get(s.cur_part,"")+" "+d

def visible_concept_words(html):
    # remove collapsed answers and svg, count words in concepts part
    m=re.search(r'data-part="concepts".*?(?=<section class="part"|\Z)',html,re.S)
    if not m: return 0
    t=re.sub(r"<svg.*?</svg>","",m.group(0),flags=re.S)
    t=re.sub(r"<details.*?</details>","",t,flags=re.S)
    t=re.sub(r"<[^>]+>"," ",t)
    return len(re.findall(r"[A-Za-z][A-Za-z'-]*",t))

def lint(uid):
    cfg={u["id"]:u for u in json.load(open(os.path.join(SITE,"units.json")))["units"]}
    if uid not in cfg: print(f"ERROR unknown unit {uid}"); return 1
    u=cfg[uid]; f=os.path.join(SITE,"content",uid+".html")
    if not os.path.exists(f): print(f"ERROR missing {f}"); return 1
    html=open(f,encoding="utf-8").read()
    p=P(); p.feed(html); p.close()
    E=p.errors; W=p.warns
    for t,l in p.stack: E.append(f"L{l}: <{t}> never closed")
    # colours anywhere inside svg source text
    for m in re.finditer(r"<svg.*?</svg>",html,re.S):
        if re.search(r"#[0-9a-fA-F]{3,8}[\"';\s)]",m.group(0)) and not re.search(r"url\(#",m.group(0)[max(0,0):]):
            E.append("literal hex colour inside an <svg>")
    if not html.lstrip().startswith(f'<section class="unit" data-unit="{uid}"'):
        E.append(f'file must start with <section class="unit" data-unit="{uid}">')
    seen={}
    for i,l in p.ids:
        if not i.startswith(uid+"-"): E.append(f"L{l}: id '{i}' does not start with '{uid}-'")
        if i in seen: E.append(f"L{l}: duplicate id '{i}' (first L{seen[i]})")
        seen[i]=l
    need=["concepts","theory"]+(["numericals"] if "numericals" in u["targets"] else [])
    got={dp:i for i,dp in p.parts}
    for n in need:
        if got.get(n)!=f"{uid}-{n}": E.append(f'missing <section class="part" id="{uid}-{n}" data-part="{n}">')
    for n in got:
        if n not in need: E.append(f"unexpected part '{n}'")
    if f"{uid}-quiz" not in seen: E.append(f"missing quiz id {uid}-quiz")
    # MathJax delimiters
    for a,b in (("\\(","\\)"),("\\[","\\]")):
        if html.count(a)!=html.count(b): E.append(f"unbalanced {a} {b}: {html.count(a)} vs {html.count(b)}")
    # raw TeX outside the delimiters would show as code to the student
    stripped=re.sub(r"<svg.*?</svg>","",html,flags=re.S)
    stripped=re.sub(r"\\\[.*?\\\]","",stripped,flags=re.S); stripped=re.sub(r"\\\(.*?\\\)","",stripped,flags=re.S)
    for m in re.finditer(r"\\[A-Za-z]{2,}",stripped):
        ln=stripped[:m.start()].count("\n")+1
        E.append(f"raw TeX '{m.group(0)}' outside \\( \\) or \\[ \\] (near: {stripped[max(0,m.start()-40):m.start()+30].strip()!r})"); break
    # images + manifest
    man_path=os.path.join(SITE,"manifest",uid+".json")
    man=[]
    if os.path.exists(man_path):
        try: man=json.load(open(man_path))
        except Exception as e: E.append(f"manifest not valid JSON: {e}")
    else: E.append("manifest file missing (write [] if no photos)")
    mfiles={m.get("file") for m in man if isinstance(m,dict)}
    for m in man:
        for k in ("file","commons_page","author","license","caption"):
            if not m.get(k): E.append(f"manifest entry {m.get('file')} missing '{k}'")
        lic=(m.get("license") or "").lower()
        if lic and not any(x in lic for x in ("public domain","cc0","cc by","cc-by","pd")):
            E.append(f"manifest {m.get('file')}: licence '{m.get('license')}' not allowed")
    for src,l in p.imgs:
        if not src.startswith(f"img/{uid}-"): E.append(f"L{l}: img src '{src}' must be img/{uid}-…")
        fp=os.path.join(SITE,src)
        if not os.path.exists(fp): E.append(f"L{l}: image file missing {src}")
        elif os.path.getsize(fp)>300_000: E.append(f"{src} is {os.path.getsize(fp)//1024} KB (>300 KB)")
        if src not in mfiles: E.append(f"L{l}: {src} not in manifest")
    for w,l in p.widgets:
        if w not in WIDGETS: E.append(f"L{l}: unknown widget '{w}'")
        elif w not in u["widgets"]: W.append(f"L{l}: widget '{w}' not listed for this unit")
    # QB coverage
    srcs=" ".join(p.qsrc)
    subj=u["subject"].upper()
    for q in u["qb"]:
        if not re.search(rf"{subj} QB Q{q}\b",srcs): E.append(f"{subj} QB Q{q} not cited in any q-src")
    for a in u["assignment"]:
        if not re.search(rf"Assignment A{a}\b",srcs): E.append(f"Assignment A{a} not cited in any q-src")
    # budgets
    b=u["budget"]; wc=visible_concept_words(html)
    lo,hi=b["concept_words"]
    if wc<lo*0.85: W.append(f"concept words {wc} below budget {lo}-{hi}")
    if wc>hi*1.15: W.append(f"concept words {wc} above budget {lo}-{hi}")
    nq=p.counts.get("q",0); qlo,qhi=b["theory_qs"]
    if nq<qlo: W.append(f"theory questions {nq} < {qlo}")
    ns=p.counts.get("num",0); npr=p.counts.get("num.practice",0)
    if "numericals" in u["targets"]:
        if ns<b["solved"][0]: W.append(f"solved numericals {ns} < {b['solved'][0]}")
        if npr<b["practice"][0]: W.append(f"practice problems {npr} < {b['practice'][0]}")
    if p.mcq<6: W.append(f"only {p.mcq} MCQs (want 6-10)")
    if p.cards<6: W.append(f"only {p.cards} flashcards (want 6-12)")
    if p.counts.get("fig",0)<4: W.append(f"only {p.counts.get('fig',0)} SVG figures")
    size=os.path.getsize(f)
    print(f"== {uid}: {size//1024} KB | concept words {wc} | figs {p.counts.get('fig',0)} (svg {p.svg_count}) | photos {len(p.imgs)} | "
          f"theory {nq} | solved {ns} | practice {npr} | mcq {p.mcq} | cards {p.cards} | widgets {[w for w,_ in p.widgets]}")
    for e in E: print("ERROR", e)
    for w in W: print("WARN ", w)
    print("RESULT:", "FAIL" if E else "PASS")
    return 1 if E else 0

if __name__=="__main__":
    rc=0
    for uid in sys.argv[1:] or []: rc|=lint(uid)
    sys.exit(rc)
