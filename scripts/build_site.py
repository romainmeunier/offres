#!/usr/bin/env python3
import re, html, shutil
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
CONTENT = BASE / "content"
PUBLIC = BASE / "public"
ASSETS = BASE / "assets"

def md_to_html(md_text: str) -> str:
    lines = md_text.splitlines()
    html_lines = []
    in_code = False
    list_open = False
    def close_list():
        nonlocal list_open
        if list_open:
            html_lines.append("</ul>")
            list_open = False
    for line in lines:
        if line.strip().startswith("```"):
            if not in_code:
                close_list()
                in_code = True
                html_lines.append("<pre><code>")
            else:
                in_code = False
                html_lines.append("</code></pre>")
            continue
        if in_code:
            html_lines.append(html.escape(line))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_list()
            level = len(m.group(1))
            text = m.group(2).strip()
            html_lines.append(f"<h{level}>{html.escape(text)}</h{level}>")
            continue
        if re.match(r"^\s*-\s+", line):
            if not list_open:
                list_open = True
                html_lines.append("<ul>")
            item = re.sub(r"^\s*-\s+", "", line)
            item_html = html.escape(item)
            item_html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", item_html)
            item_html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", item_html)
            html_lines.append(f"<li>{item_html}</li>")
            continue
        else:
            if list_open and line.strip() == "":
                close_list()
        if line.strip() == "":
            html_lines.append("")
        else:
            txt = html.escape(line)
            txt = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", txt)
            txt = re.sub(r"\*(.+?)\*", r"<em>\1</em>", txt)
            txt = re.sub(r"`([^`]+)`", r"<code>\1</code>", txt)
            html_lines.append(f"<p>{txt}</p>")
    close_list()
    return "\n".join(html_lines)

BASE_HTML = (BASE / "base.html").read_text(encoding="utf-8")

def render_page(lang, heading, body_html):
    contact = "Contact: romainmeunier@gmail.com · +593 95 890 9378 · Project $900/day (~€830) · Retainer $800/day (~€740) — USD + EUR"
    title = "Romain Meunier — SRE & Kubernetes Offers"
    desc = "SRE & Kubernetes offers, SOW, brochures — tool-agnostic, platform-agnostic. Quito (UTC-5)."
    return BASE_HTML.format(
        lang=lang, title=title, desc=desc, heading=heading, contact=contact,
        body=body_html, year=datetime.now().year,
        fr_active="active" if lang=="fr" else "", en_active="active" if lang=="en" else ""
    )

def list_files_by_lang(folder: Path, suffix=".md"):
    files = [f for f in folder.glob(f"*{suffix}") if f.is_file()]
    out = {"fr": [], "en": []}
    for f in files:
        lang = "fr" if f.stem.endswith("_FR") else ("en" if f.stem.endswith("_EN") else "fr")
        out[lang].append(f)
    return out

def card_html(locale, offers_by_lang, sow_by_lang, brochures_dir):
    CARD_ORDER = [
        ("SRE_01", "SRE‑01 — Strategy & Operating Model", "SLI/SLO, on‑call, alerting policy."),
        ("SRE_02", "SRE‑02 — Observability, SLOs & Incident Ops", "Platform/tool‑agnostic. K8s optional."),
        ("K1", "K1 — Kubernetes — Deployments & GitOps", "Predictable & reversible releases."),
        ("K2", "K2 — Kubernetes — Resource Optimization", "FinOps + Resilience."),
        ("K3", "K3 — Kubernetes — Architecture & Lifecycle", "Control‑plane assessment."),
        ("D", "D — Kubernetes — GitOps for Cloud Infra", "Infra as API (XRD/Compositions)."),
        ("R", "R — SRE Retainer", "2/4/6 days per month.")
    ]
    rows = []
    for key, title, blurb in CARD_ORDER:
        off = next((f for f in offers_by_lang[locale] if f.name.startswith(key)), None)
        sw = next((f for f in sow_by_lang[locale] if f.name.startswith(key)), None)
        bros = next((f for f in brochures_dir.glob(f"{key}_{locale.upper()}.html")), None)
        if off or sw or bros:
            if locale == "fr":
                htitle = (title
                          .replace("Deployments", "Déploiements")
                          .replace("Resource Optimization","Optimisation Ressources")
                          .replace("Architecture & Lifecycle","Architecture & Cycle de vie")
                          .replace("for Cloud Infra","pour Infra Cloud")
                          .replace("SRE Retainer","Rétainer SRE"))
                hblurb = (blurb
                          .replace("Predictable & reversible releases.","Releases prévisibles & réversibles.")
                          .replace("Resource Optimization","Optimisation Ressources")
                          .replace("Control‑plane assessment.","Assessment control‑plane.")
                          .replace("2/4/6 days per month.","2/4/6 j par mois.")
                          .replace("Platform/tool‑agnostic. K8s optional.","Platform/tool‑agnostique. K8s en option."))
            else:
                htitle, hblurb = title, blurb
            row = f'''
            <div class="card" data-card="{htitle} {hblurb}">
              <h3>{htitle}</h3>
              <p>{hblurb}</p>
              <div class="pills">
                {f'<a href="offers/{off.name.replace(".md",".html")}">Offer</a>' if off else ''}
                {f'<a href="sow/{sw.name.replace(".md",".html")}">SOW</a>' if sw else ''}
                {f'<a href="brochures/{bros.name}">Brochure</a>' if bros else ''}
              </div>
            </div>'''
            rows.append(row)
    return '<div class="grid">' + "\n".join(rows) + "</div>"

def build():
    # Reset public
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    (PUBLIC/"offers").mkdir(parents=True, exist_ok=True)
    (PUBLIC/"sow").mkdir(parents=True, exist_ok=True)
    (PUBLIC/"brochures").mkdir(parents=True, exist_ok=True)
    (PUBLIC/"assets").mkdir(parents=True, exist_ok=True)

    # Copy assets
    shutil.copy2(ASSETS/"style.css", PUBLIC/"assets"/"style.css")
    shutil.copy2(ASSETS/"app.js", PUBLIC/"assets"/"app.js")

    offers_dir = CONTENT/"offers"
    sow_dir = CONTENT/"sow"
    broch_dir = CONTENT/"brochures"

    # Render MD files
    def render_md_file(md_path: Path, lang: str, subdir: str):
        md = md_path.read_text(encoding="utf-8")
        body = md_to_html(md)
        body_html = f'<div class="content"><div class="meta">Source: {md_path.name}</div>{body}</div>'
        out_name = md_path.with_suffix(".html").name
        out_dir = PUBLIC / subdir
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir/out_name).write_text(render_page(lang, md_path.stem, body_html), encoding="utf-8")

    for f in offers_dir.glob("*.md"):
        render_md_file(f, "fr" if f.name.endswith("_FR.md") else "en", "offers")
    for f in sow_dir.glob("*.md"):
        render_md_file(f, "fr" if f.name.endswith("_FR.md") else "en", "sow")

    # Copy brochures
    for f in broch_dir.glob("*.html"):
        shutil.copy2(f, PUBLIC/"brochures"/f.name)

    # Index
    offers_by_lang = {"fr": [*offers_dir.glob("*_FR.md")], "en": [*offers_dir.glob("*_EN.md")]}
    sow_by_lang = {"fr": [*sow_dir.glob("*_FR.md")], "en": [*sow_dir.glob("*_EN.md")]}
    search_html = (
        '<div class="search">'
        '<input type="search" id="q" placeholder="Search offers, keywords, tools…">'
        '<a class="btn" href="mailto:romainmeunier@gmail.com?subject=Inquiry%20—%20SRE%20%26%20Kubernetes">Book a call</a>'
        '</div>'
        '<div data-locale="fr" style="display:none">' + card_html("fr", offers_by_lang, sow_by_lang, broch_dir) + '</div>'
        '<div data-locale="en">' + card_html("en", offers_by_lang, sow_by_lang, broch_dir) + '</div>'
    )
    (PUBLIC/"index.html").write_text(render_page("en","SRE & Kubernetes Offers — FR/EN", search_html), encoding="utf-8")

if __name__ == "__main__":
    build()
