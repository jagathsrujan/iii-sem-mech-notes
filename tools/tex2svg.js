// Convert every \( … \) and \[ … \] in an HTML fragment to inline MathJax SVG.
// Usage: node tex2svg.js in.html out.html   (prints a report; exit 1 on any TeX error)
const fs = require("fs");
const {mathjax} = require("mathjax-full/js/mathjax.js");
const {TeX} = require("mathjax-full/js/input/tex.js");
const {SVG} = require("mathjax-full/js/output/svg.js");
const {liteAdaptor} = require("mathjax-full/js/adaptors/liteAdaptor.js");
const {RegisterHTMLHandler} = require("mathjax-full/js/handlers/html.js");
const {AllPackages} = require("mathjax-full/js/input/tex/AllPackages.js");

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const tex = new TeX({packages: AllPackages.filter(p => p !== "bussproofs"), formatError: (jax, err) => { throw err; }});
const svg = new SVG({fontCache: "global"});
const doc = mathjax.document("", {InputJax: tex, OutputJax: svg});

const dec = s => s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&");
const [, , inp, out] = process.argv;
let html = fs.readFileSync(inp, "utf8");
let n = 0, errs = [];
function conv(src, display) {
  const t = dec(src).trim();
  try {
    const node = doc.convert(t, {display, em: 18, ex: 8, containerWidth: 700});
    let s = adaptor.innerHTML(node);              // the <svg> element
    s = s.replace(/<svg /, `<svg aria-label="${t.replace(/"/g, "'").replace(/</g, "&lt;").replace(/>/g, "&gt;")}" `);
    n++;
    return display ? `<span class="md">${s}</span>` : `<span class="mi">${s}</span>`;
  } catch (e) {
    errs.push(`${display ? "\\[" : "\\("} ${t.slice(0, 80)} …  → ${e.message}`);
    return display ? `<span class="md">${src}</span>` : src;
  }
}
// display first, then inline. Skip content inside <svg>…</svg> figures.
const parts = html.split(/(<svg[\s\S]*?<\/svg>)/);
for (let i = 0; i < parts.length; i += 2) {
  parts[i] = parts[i].replace(/\\\[([\s\S]+?)\\\]/g, (m, a) => conv(a, true))
                     .replace(/\\\(([\s\S]+?)\\\)/g, (m, a) => conv(a, false));
}
html = parts.join("");
const cache = svg.fontCache.getCache ? adaptor.outerHTML(svg.fontCache.getCache()) : "";
if (cache) html = html.replace(/(<section class="unit"[^>]*>)/, `$1<svg class="mjx-cache" width="0" height="0" aria-hidden="true" focusable="false">${cache}</svg>`);
fs.writeFileSync(out, html);
const left = (html.replace(/<svg[\s\S]*?<\/svg>/g, "").match(/\\\(|\\\[/g) || []).length;
console.log(`formulas converted: ${n}; TeX errors: ${errs.length}; raw delimiters left: ${left}; size ${(html.length/1024)|0} KB`);
errs.forEach(e => console.log("TEXERR " + e));
process.exit(errs.length || left ? 1 : 0);
