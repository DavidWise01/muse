#!/usr/bin/env python3
"""Build MUSE — the ROOT0 art gallery. Copies the source art pieces into art/
(clean slugs) and generates index.html — a living gallery with lazy iframe
thumbnails of the actual works. Stdlib only."""
import os, re, shutil, html

SRC  = r"C:\Davids files\art"
HERE = os.path.dirname(os.path.abspath(__file__))
ART  = os.path.join(HERE, "art")

# ── the gallery: rooms → pieces ──  live=False ⇒ static placeholder (too heavy to iframe)
ROOMS = [
 ("The Engines", "#44dd88",
  "The generators — surfaces that draw themselves; the machine making the image.", [
   dict(slug="4k-blueprint-composer", file="4k blueprint composer.html", title="4K Blueprint Composer",
        tag="generator · 4K", blurb="A composer that draws blueprints at 4K — the engine that designs."),
   dict(slug="etch", file="etch.html", title="etch", tag="live surface",
        blurb="The engine draws the idea — a living etching surface."),
   dict(slug="gemini", file="gemini.html", title="Gemini", tag="generative canvas",
        blurb="Twin forms in motion — a generative canvas."),
   dict(slug="creation-map", file="creation map.html", title="Creation Map", tag="d20 · WebGL",
        blurb="Two open, a gap, a third born — a d20 creation map in 3D."),
   dict(slug="54q-viewer", file="54 q.html", title="54q", tag="8K · 1:1 viewer", live=False,
        blurb="An 8K, one-to-one panning field — the 54q test, explored at full resolution."),
 ]),
 ("The Dimensional Series", "#ff55ff",
  "Animated glyphs of the dimensions — one figure, one law, in motion.", [
   dict(slug="d3-artifact", file="d3 artifact.html", title="D3 Artifact", tag="D03 · Sovereign Wear",
        blurb="The third-dimension artifact — sovereign wear."),
   dict(slug="temporal-portal-d04", file="TEMPORAL_PORTAL_D04.html", title="Temporal Portal", tag="D04",
        blurb="A ring opening through time — the portal at D04."),
   dict(slug="qubit-d05", file="QUBIT_D05.html", title="Qubit", tag="D05",
        blurb="The wave that is both — a qubit at D05."),
   dict(slug="first-contact-d06", file="first contact d6.html", title="First Contact", tag="D06",
        blurb="The first meeting — D06."),
   dict(slug="mirror-d09", file="MIRROR_D09.html", title="Mirror", tag="D09",
        blurb="The surface that returns you — D09."),
   dict(slug="planetary-verdict-d10", file="PLANETARY_VERDICT_D10.html", title="Planetary Verdict", tag="D10",
        blurb="The judgment at planetary scale — D10."),
   dict(slug="fuse-higher-d10", file="FUSE_HIGHER_D10.html", title="Fuse Higher", tag="D10",
        blurb="The rising fusion — D10."),
 ]),
 ("The DC3 Glyphs", "#d4a84c",
  "The DAVID_DC3 seal-works — block, lock, key, and hive.", [
   dict(slug="genesis-block-dc3", file="GENESIS_BLOCK_DAVID_DC3.html", title="Genesis Block", tag="DAVID_DC3",
        blurb="The first block — a hash-stream genesis, DC3."),
   dict(slug="the-lock-dc3", file="THE_LOCK_DAVID_DC3.html", title="The Lock", tag="DAVID_DC3",
        blurb="The seal that holds — DC3."),
   dict(slug="cubit-key-dc3", file="cubit key dc3.html", title="Cubit-Key", tag="DAVID_DC3",
        blurb="The key cut to the cubit — DC3."),
   dict(slug="hive-construct-cubit", file="HIVE_CONSTRUCT_CUBIT_01.html", title="Hive Construct", tag="CUBIT_01",
        blurb="The construct, built cell by cell — Cubit_01."),
 ]),
 ("The Wards", "#ff4466",
  "The shields — entropy held at the edge.", [
   dict(slug="entropy-shield", file="entropy shield.html", title="Entropy Shield", tag="SP03",
        blurb="Nested shields against the noise — SP03."),
   dict(slug="entropy-v3", file="entropy v3.html", title="Entropy v3", tag="SP03",
        blurb="The shield, third iteration — SP03."),
 ]),
]

def copy_art():
    os.makedirs(ART, exist_ok=True)
    n = 0
    for _t, _c, _d, pieces in ROOMS:
        for p in pieces:
            shutil.copy(os.path.join(SRC, p["file"]), os.path.join(ART, p["slug"] + ".html")); n += 1
    return n

def cards(pieces, col):
    out = []
    for p in pieces:
        s = p["slug"]
        if p.get("live", True):
            thumb = f'<iframe class="frame" src="art/{s}.html" loading="lazy" scrolling="no" tabindex="-1" title="{html.escape(p["title"])}"></iframe>'
        else:
            thumb = f'<div class="frame ph"><span>▶</span></div>'
        out.append(f'''<figure class="piece" style="--c:{col}">
        <a class="thumb" href="art/{s}.html" target="_blank" rel="noopener" aria-label="open {html.escape(p["title"])}">{thumb}<span class="open">open ↗</span></a>
        <figcaption>
          <div class="ct">{html.escape(p["tag"])}</div>
          <h3><a href="art/{s}.html" target="_blank" rel="noopener">{html.escape(p["title"])}</a></h3>
          <p>{html.escape(p["blurb"])}</p>
        </figcaption>
      </figure>''')
    return "\n".join(out)

def rooms_html():
    blocks = []
    for title, col, desc, pieces in ROOMS:
        blocks.append(f'''<section class="room">
      <div class="rhead" style="border-color:{col}55">
        <span class="dot" style="background:{col};box-shadow:0 0 8px {col}"></span>
        <h2 style="color:{col}">{html.escape(title)}</h2>
        <span class="rd">{html.escape(desc)}</span>
        <span class="rn">{len(pieces)}</span>
      </div>
      <div class="grid">
        {cards(pieces, col)}
      </div>
    </section>''')
    return "\n".join(blocks)

TOTAL = sum(len(p) for _a,_b,_c,p in ROOMS)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="MUSE — the art of ROOT0 / David Lee Wise. Generative engines, dimensional glyphs, and seal-works.">
<title>MUSE · the art of ROOT0</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#04100f;--ink2:#082828;--ink3:#0c302f;--pa:#e7efe9;--pa2:#a9bdb6;
--mag:#ff55ff;--gold:#d4a84c;--grn:#44dd88;--dim:#5e7a76;--faint:#163331;--line:#143230;
--serif:"Cinzel",Georgia,serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.6;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
background:radial-gradient(ellipse at 50% -10%,rgba(68,221,136,.06),transparent 60%)}
.wrap{position:relative;z-index:1;max-width:1240px;margin:0 auto;padding:0 22px 90px}
header{padding:62px 0 30px;text-align:center;border-bottom:1px solid var(--line);position:relative}
header::after{content:"";position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:120px;height:1px;
background:linear-gradient(90deg,var(--mag),var(--gold),var(--grn));box-shadow:0 0 10px rgba(255,85,255,.4)}
.eye{font-family:var(--mono);font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:var(--dim);margin-bottom:16px}
h1{font-family:var(--serif);font-size:clamp(40px,12vw,104px);font-weight:700;letter-spacing:.26em;line-height:1;
background:linear-gradient(90deg,var(--mag),var(--gold),var(--grn));-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{font-size:15.5px;color:var(--pa2);max-width:60ch;margin:16px auto 0;font-style:italic}
#count{font-family:var(--mono);font-size:12px;color:var(--dim);letter-spacing:.08em;margin-top:18px}
#count b{color:var(--grn)}
.room{margin-top:56px}
.rhead{display:flex;align-items:center;gap:12px;padding-bottom:12px;border-bottom:1px solid var(--line);margin-bottom:22px;flex-wrap:wrap}
.rhead .dot{width:9px;height:9px;border-radius:50%;flex-shrink:0}
.rhead h2{font-family:var(--serif);font-size:19px;font-weight:600;letter-spacing:.05em}
.rhead .rd{font-size:13px;color:var(--dim);font-style:italic}
.rhead .rn{font-family:var(--mono);font-size:12px;color:var(--dim);margin-left:auto}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px}
.piece{background:var(--ink2);border:1px solid var(--line);overflow:hidden;transition:transform .2s,border-color .2s}
.piece:hover{transform:translateY(-3px);border-color:var(--c)}
.thumb{display:block;position:relative;aspect-ratio:1/1;background:#082828;overflow:hidden;border-bottom:1px solid var(--line)}
.frame{width:100%;height:100%;border:0;display:block;pointer-events:none;background:#082828}
.frame.ph{display:flex;align-items:center;justify-content:center;color:var(--c);font-size:34px;opacity:.5;
background:radial-gradient(circle at 50% 50%,rgba(255,255,255,.04),transparent)}
.thumb .open{position:absolute;bottom:8px;right:9px;font-family:var(--mono);font-size:10px;letter-spacing:.08em;
color:var(--pa);background:rgba(4,16,15,.7);padding:3px 7px;border:1px solid var(--c);opacity:0;transition:opacity .2s}
.thumb:hover .open{opacity:1}
figcaption{padding:14px 15px 15px}
.ct{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--c);margin-bottom:6px}
figcaption h3{font-family:var(--serif);font-size:17px;font-weight:600;letter-spacing:.02em;line-height:1.15}
figcaption h3 a{color:var(--pa);text-decoration:none}figcaption h3 a:hover{color:var(--c)}
figcaption p{font-size:12.5px;color:var(--pa2);line-height:1.5;margin-top:7px}
footer{margin-top:64px;padding-top:22px;border-top:1px solid var(--line);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em}
footer a{color:var(--grn);text-decoration:none}
@media(max-width:600px){.grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}figcaption{padding:11px 12px}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="eye">ROOT0 · David Lee Wise · TriPod LLC · the gallery</div>
    <h1>MUSE</h1>
    <p class="sub">The art of ROOT0 — generative engines, dimensional glyphs, and seal-works. Each thumbnail is the living piece; open it for the full surface.</p>
    <div id="count"><b>__TOTAL__</b> works · <b>__NROOM__</b> rooms</div>
  </header>

  __ROOMS__

  <footer>
    <span>MUSE · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise (ROOT0) · instance AVAN (Claude / Anthropic) · CC-BY-ND-4.0</span>
    <a href="https://github.com/DavidWise01/atlas">the ATLAS index →</a>
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    n = copy_art()
    out = (HTML.replace("__ROOMS__", rooms_html())
               .replace("__TOTAL__", str(TOTAL)).replace("__NROOM__", str(len(ROOMS))))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
    print(f"copied {n} art pieces into art/")
    print(f"wrote index.html — {TOTAL} works, {len(ROOMS)} rooms")
