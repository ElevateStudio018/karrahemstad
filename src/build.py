#!/usr/bin/env python3
"""Builds the static site into public/.  Usage: python3 src/build.py

Preview under a sub path (GitHub Pages): BASE_PATH=/karrahemstad/preview/ OUT_DIR=preview python3 src/build.py
"""
import json
import os
import shutil
from datetime import date
from html import escape as e
from pathlib import Path

from PIL import Image

from content import (ABOUT, COMPANY, DOCS, FAQ, FORM_ENDPOINT, GUARANTEES, MOVING,
                     SERVICES, SITE_URL)

SRC = Path(__file__).parent
OUT = SRC.parent / os.environ.get("OUT_DIR", "public")
# Site root on the server. "/" in production; a sub path for previews.
BASE = os.environ.get("BASE_PATH", "/")
ASSET_VERSION = date.today().strftime("%Y%m%d")
BY_SLUG = {s["slug"]: s for s in SERVICES}
PRIVATE = [s for s in SERVICES if not s["business"]]
BUSINESS = [s for s in SERVICES if s["business"]]


def kr(n):
    return f"{n:,}".replace(",", " ") + " kr"


def price_label(s):
    return s.get("price_label") or f"{s['hour']} kr/h"


def price_suffix(s):
    return "ex. moms" if s["business"] else "efter RUT"


def price_head(s):
    if s["slug"] in ("industristadning", "trappstadning"):
        return f'Från {s["hour"]}&nbsp;kr/h'
    return price_label(s)


# --------------------------------------------------------------------- icons

def icon(name, cls="i"):
    paths = {
        "phone": '<path d="M6.6 3.5 9 3l1.6 4-2 1.3a10 10 0 0 0 5.1 5.1L15 11.4l4 1.6-.5 2.4A2 2 0 0 1 16.6 17 13.6 13.6 0 0 1 3 3.4 2 2 0 0 1 4.6 1.5" transform="translate(1.5 2.5)"/>',
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6 8.5 7 8.5-7"/>',
        "pin": '<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
        "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
        "close": '<path d="M6 6l12 12M18 6 6 18"/>',
        "down": '<path d="m6 9 6 6 6-6"/>',
        "file": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
        "shield": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.3 7.5 9.5 4.3-1.2 7.5-4.9 7.5-9.5V6z"/><path d="m8.8 12 2.3 2.3 4.2-4.6"/>',
        "doc": '<path d="M6 3h9l3 3v15H6z"/><path d="M9 9h6M9 13h6M9 17h4"/>',
        "badge": '<circle cx="12" cy="9" r="6"/><path d="m8.5 14 -1.5 7 5-2.5 5 2.5-1.5-7"/><path d="m9.5 9 1.8 1.8L14.8 7.5"/>',
        "leaf": '<path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19c3-4 6-7 10-9"/>',
        "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4.5 4.4-7 8-7s7 2.5 8 7"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    }
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>')


def picture(name, alt, sizes, cls="", eager=False, pos=None):
    style = f' style="object-position:{pos}"' if pos else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="/assets/img/{name}-1200.webp" '
            f'srcset="/assets/img/{name}-640.webp 640w, /assets/img/{name}-1200.webp 1200w, /assets/img/{name}-1920.webp 1920w" '
            f'sizes="{sizes}" alt="{e(alt)}" width="1200" height="675" {load}{style}>')


# --------------------------------------------------------------------- layout

def head(title, desc, path, jsonld=()):
    url = SITE_URL + path
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    return f"""<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="sv_SE">
<meta property="og:site_name" content="{COMPANY['name']}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b1f3a">
<link rel="icon" href="/assets/img/icon-32.png" sizes="32x32">
<link rel="icon" href="/assets/img/icon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={ASSET_VERSION}">
<script>document.documentElement.classList.add("js")</script>
<script src="/assets/js/main.js?v={ASSET_VERSION}" defer></script>
{ld}
</head>"""


def header(active="", overlay=True):
    def links(items):
        return "".join(
            f'<li><a href="/{s["slug"]}/"{" aria-current=page" if active == s["slug"] else ""}>'
            f'<span>{s["name"]}</span><small>{price_label(s)}</small></a></li>' for s in items)

    is_service = active in BY_SLUG

    def cur(key):
        return ' aria-current="page"' if active == key else ""

    return f"""<body class="{'has-overlay' if overlay else 'no-overlay'}">
<a class="skip" href="#main">Hoppa till innehållet</a>
<header class="site-header">
  <div class="topbar">
    <div class="wrap topbar-row">
      <span>{icon('pin', 'i i-xs')} {COMPANY['area']}</span>
      <span class="topbar-right">
        <a href="mailto:{COMPANY['email']}">{icon('mail', 'i i-xs')} {COMPANY['email']}</a>
        <a href="{COMPANY['phone_href']}">{icon('phone', 'i i-xs')} {COMPANY['phone']}</a>
      </span>
    </div>
  </div>
  <div class="wrap header-row">
    <a class="logo" href="/" aria-label="{COMPANY['name']} – startsidan">
      <img src="/assets/img/logo.png" alt="{COMPANY['name']}" width="180" height="40">
    </a>
    <nav class="nav" id="nav" aria-label="Huvudmeny">
      <ul class="nav-list">
        <li class="has-sub">
          <button class="nav-sub-toggle" aria-expanded="false" aria-controls="sub-services"{' data-active' if is_service else ''}>Tjänster {icon('down', 'i i-sm')}</button>
          <div class="sub" id="sub-services">
            <div class="sub-col"><p class="sub-h">Privat</p><ul>{links(PRIVATE)}</ul></div>
            <div class="sub-col"><p class="sub-h">Företag &amp; föreningar</p><ul>{links(BUSINESS)}</ul></div>
          </div>
        </li>
        <li><a href="/#flyttjanst">Flytthjälp</a></li>
        <li><a href="/#priser">Priser</a></li>
        <li><a href="/om-oss/"{cur('om-oss')}>Om oss</a></li>
        <li><a href="/kontakta-oss/"{cur('kontakta-oss')}>Kontakt</a></li>
      </ul>
    </nav>
    <div class="header-cta">
      <a class="phone-link" href="{COMPANY['phone_href']}" aria-label="Ring {COMPANY['phone']}">{icon('phone')}</a>
      <a class="btn btn-primary btn-sm" href="#offert" data-quote>Begär offert</a>
      <button class="menu-btn" aria-expanded="false" aria-controls="nav" aria-label="Meny">{icon('menu', 'i i-open')}{icon('close', 'i i-close')}</button>
    </div>
  </div>
</header>
<main id="main">"""


def footer(cta_band=False):
    priv = "".join(f'<li><a href="/{s["slug"]}/">{s["name"]}</a></li>' for s in PRIVATE)
    biz = "".join(f'<li><a href="/{s["slug"]}/">{s["name"]}</a></li>' for s in BUSINESS)
    band = f"""<section class="cta-band">
  <div class="wrap cta-band-row">
    <div>
      <p class="cta-band-title">Redo att slippa städningen?</p>
      <p>Få en kostnadsfri offert – eller ring oss direkt.</p>
    </div>
    <div class="cta-band-actions">
      <a class="btn btn-primary btn-lg" href="#offert" data-quote>Begär offert {icon('arrow')}</a>
      <a class="btn btn-outline-light btn-lg" href="{COMPANY['phone_href']}">{icon('phone')} {COMPANY['phone']}</a>
    </div>
  </div>
</section>""" if cta_band else ""
    return f"""</main>
{band}
<footer class="site-footer">
  <div class="wrap footer-top">
    <div class="footer-brand">
      <img src="/assets/img/logo.png" alt="{COMPANY['name']}" width="180" height="40">
      <p>Det lokala städbolaget i Kärra. Städning för hem, företag och bostadsrättsföreningar på {COMPANY['area']}.</p>
      <p class="social">
        <a href="{COMPANY['facebook']}" rel="noopener">Facebook</a>
        <a href="{COMPANY['instagram']}" rel="noopener">Instagram</a>
      </p>
    </div>
    <div>
      <p class="footer-h">Privat</p>
      <ul>{priv}</ul>
    </div>
    <div>
      <p class="footer-h">Företag</p>
      <ul>{biz}<li><a href="/#flyttjanst">Flytthjälp</a></li></ul>
    </div>
    <div>
      <p class="footer-h">Kontakt</p>
      <ul class="footer-contact">
        <li><a href="{COMPANY['phone_href']}">{icon('phone', 'i i-sm')}{COMPANY['phone']}</a></li>
        <li><a href="mailto:{COMPANY['email']}">{icon('mail', 'i i-sm')}{COMPANY['email']}</a></li>
        <li><a href="{COMPANY['maps']}" rel="noopener">{icon('pin', 'i i-sm')}<span>{COMPANY['street']}<br>{COMPANY['zip']} {COMPANY['city']}</span></a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="wrap footer-bottom-row">
      <span>© {date.today().year} {COMPANY['legal']}</span>
      <span class="footer-links"><a href="/om-oss/">Om oss</a><a href="/#fragor">Vanliga frågor</a><a href="/{DOCS['nyckel'][1]}">Nyckelkvittens (PDF)</a></span>
    </div>
  </div>
</footer>
<div class="mobile-bar" aria-label="Snabbkontakt">
  <a class="btn btn-ghost" href="{COMPANY['phone_href']}">{icon('phone')} Ring</a>
  <a class="btn btn-primary" href="#offert" data-quote>Begär offert</a>
</div>
</body>
</html>
"""


def page(title, desc, path, body, active="", jsonld=(), overlay=True):
    return head(title, desc, path, jsonld) + header(active, overlay) + body + footer(cta_band='id="offert"' not in body or 'class="aside"' in body)


# --------------------------------------------------------------------- components

def section_head(kicker, title, text="", center=False, light=False):
    t = f'<p class="lede">{text}</p>' if text else ""
    cls = "section-head" + (" center" if center else "") + (" light" if light else "")
    return f'<div class="{cls}"><p class="kicker">{kicker}</p><h2>{title}</h2>{t}</div>'


def calculator():
    data = [{"slug": s["slug"], "name": s["name"], "hour": s["hour"], "kvm": s["kvm"], "business": s["business"]}
            for s in SERVICES]
    kvm_opts = "".join(f'<option value="{s["slug"]}">{s["name"]}</option>' for s in SERVICES if s["kvm"])
    return f"""<div class="calc" data-calc>
  <script type="application/json" data-calc-data>{json.dumps(data, ensure_ascii=False)}</script>
  <div class="calc-head">
    <p class="calc-title">Räkna på priset</p>
    <div class="seg" role="radiogroup" aria-label="Räkna på">
      <label><input type="radio" name="calc-mode" value="kvm" checked><span>Per kvm</span></label>
      <label><input type="radio" name="calc-mode" value="hour"><span>Per timme</span></label>
    </div>
  </div>
  <label class="field calc-svc">
    <span class="label">Tjänst</span>
    <select data-calc-service>{kvm_opts}</select>
  </label>
  <div class="field calc-amt">
    <label class="label" for="calc-amount" data-calc-amount-label>Bostadens storlek</label>
    <div class="amount">
      <input id="calc-amount" type="range" min="20" max="250" step="5" value="70" data-calc-range>
      <div class="amount-num"><input type="number" inputmode="numeric" min="1" value="70" data-calc-number aria-label="Antal"><span data-calc-unit>kvm</span></div>
    </div>
  </div>
  <div class="calc-out" aria-live="polite">
    <span class="label">Ditt pris</span>
    <span class="calc-total" data-calc-total>1&nbsp;750&nbsp;kr</span>
    <span class="calc-note" data-calc-note>efter RUT, inkl. moms och material</span>
  </div>
  <a class="btn btn-primary btn-lg calc-cta" href="#offert" data-calc-cta>Begär offert {icon('arrow')}</a>
</div>"""


def quote_form(selected=None, heading="Begär offert", compact=False):
    services = SERVICES + [{"slug": "flytthjalp", "name": "Flytthjälp", "property": None},
                           {"slug": "annat", "name": "Annat / vet inte", "property": None}]
    opts = "".join(
        f'<option value="{s["name"]}" data-slug="{s["slug"]}"{" selected" if s["slug"] == selected else ""}>{s["name"]}</option>'
        for s in services)
    sel = BY_SLUG.get(selected)
    props = sel["property"] if sel else ["Lägenhet", "Radhus", "Hus", "Fritidshus", "Kontor", "Butik",
                                          "Restaurang", "Industri/Lager", "Bostadsrättsförening"]
    prop_opts = "".join(f'<option>{p}</option>' for p in props)
    prop_map = {s["slug"]: s["property"] for s in SERVICES}
    return f"""<form class="quote{' quote-compact' if compact else ''}" data-quote-form data-endpoint="{e(FORM_ENDPOINT)}" data-email="{COMPANY['email']}" novalidate>
  <script type="application/json" data-prop-map>{json.dumps(prop_map, ensure_ascii=False)}</script>
  <div class="quote-head">
    <p class="quote-title">{heading}</p>
    <div class="quote-progress" aria-hidden="true"><span data-step-label>Steg 1 av 2</span><i><b></b></i></div>
  </div>
  <fieldset class="step" data-step="1">
    <legend class="sr-only">Om uppdraget</legend>
    <label class="field"><span class="label">Tjänst</span><select name="tjanst" required>{opts}</select></label>
    <div class="row-2">
      <label class="field"><span class="label">Typ av lokal</span><select name="lokal">{prop_opts}</select></label>
      <label class="field"><span class="label">Storlek <span class="opt">(kvm)</span></span><input name="kvm" type="number" inputmode="numeric" min="1" placeholder="t.ex. 70"></label>
    </div>
    <div class="row-2">
      <label class="field"><span class="label">Postnummer eller ort</span><input name="ort" autocomplete="postal-code" placeholder="t.ex. 425 30"></label>
      <label class="field"><span class="label">Önskat datum <span class="opt">(valfritt)</span></span><input name="datum" type="date"></label>
    </div>
    <button class="btn btn-primary btn-block btn-lg" type="button" data-next>Fortsätt {icon('arrow')}</button>
  </fieldset>
  <fieldset class="step" data-step="2">
    <legend class="sr-only">Kontaktuppgifter</legend>
    <label class="field"><span class="label">Namn</span><input name="namn" autocomplete="name" required></label>
    <div class="row-2">
      <label class="field"><span class="label">Telefon</span><input name="telefon" type="tel" autocomplete="tel" required></label>
      <label class="field"><span class="label">E-post <span class="opt">(valfritt)</span></span><input name="epost" type="email" autocomplete="email"></label>
    </div>
    <label class="field"><span class="label">Något vi bör veta? <span class="opt">(valfritt)</span></span><textarea name="meddelande" rows="3" placeholder="Antal rum, husdjur, nyckel, parkering …"></textarea></label>
    <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="step-actions">
      <button class="btn btn-ghost btn-lg" type="button" data-back>Tillbaka</button>
      <button class="btn btn-primary btn-lg" type="submit">Skicka förfrågan</button>
    </div>
    <p class="form-error" role="alert" data-error hidden></p>
  </fieldset>
  <div class="quote-done" data-done hidden tabindex="-1">
    <span class="done-icon">{icon('check')}</span>
    <p class="quote-title">Tack! Vi hör av oss.</p>
    <p>Vi kontaktar dig så snart vi kan. Brådskande? Ring <a href="{COMPANY['phone_href']}">{COMPANY['phone']}</a>.</p>
  </div>
  <p class="quote-fine">{icon('shield', 'i i-xs')} Kostnadsfritt och inte bindande.</p>
</form>"""


def checklist(items):
    return '<ul class="checks">' + "".join(f'<li>{icon("check")}<span>{e(i)}</span></li>' for i in items) + "</ul>"


GUARANTEE_ICONS = ["badge", "shield", "doc", "user", "leaf"]


def guarantees_block():
    items = "".join(
        f'<li><span class="g-icon">{icon(GUARANTEE_ICONS[i])}</span><div><h3>{t}</h3><p>{d}</p></div></li>'
        for i, (t, d) in enumerate(GUARANTEES))
    return f'<ul class="guarantees">{items}</ul>'


def facts_band():
    facts = [("doc", "Kollektivavtal", "Ordnade villkor för personalen"),
             ("shield", "Ansvarsförsäkrade", "Fullt skydd för person och egendom"),
             ("badge", "Kvalitetsgaranti", "Vi gör om det tills du godkänner"),
             ("leaf", "Miljömärkt", "Miljömärkta städmedel ingår")]
    return '<ul class="facts">' + "".join(
        f'<li><span class="f-icon">{icon(i)}</span><span><strong>{t}</strong><small>{d}</small></span></li>'
        for i, t, d in facts) + "</ul>"


def faq_block(items):
    return '<div class="faq">' + "".join(
        f'<details><summary>{q}<span class="faq-plus" aria-hidden="true"></span></summary><p>{a}</p></details>'
        for q, a in items) + "</div>"


def service_card(s):
    return f"""<li><a class="card" href="/{s['slug']}/">
  <span class="card-media">{picture(s['img'], '', '(min-width: 1100px) 300px, (min-width: 700px) 50vw, 100vw', 'cover', pos=s.get('img_pos'))}
    <span class="card-price">{price_label(s)} <small>{price_suffix(s)}</small></span></span>
  <span class="card-body">
    <span class="card-title">{s['name']}</span>
    <span class="card-text">{s['lead']}</span>
    <span class="card-more">Läs mer {icon('arrow')}</span>
  </span>
</a></li>"""


def banner(img, kicker, title, lead, crumbs, extra="", pos=None, tall=False):
    crumb_html = '<a href="/">Hem</a>' + "".join(
        f'<span>/</span>{f"<a href={h}>{n}</a>" if h else f"<span>{n}</span>"}' for n, h in crumbs)
    return f"""<section class="banner{' banner-tall' if tall else ''}">
  {picture(img, '', '100vw', 'banner-img', eager=True, pos=pos)}
  <div class="wrap banner-inner">
    <nav class="crumbs" aria-label="Brödsmulor">{crumb_html}</nav>
    <p class="kicker">{kicker}</p>
    <h1>{title}</h1>
    <p class="lede">{lead}</p>
    {extra}
  </div>
</section>"""


def local_business():
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": SITE_URL + "/#company",
        "name": COMPANY["name"],
        "legalName": COMPANY["legal"],
        "url": SITE_URL + "/",
        "logo": SITE_URL + "/assets/img/logo.png",
        "image": SITE_URL + "/assets/img/og.jpg",
        "telephone": "+46 31 27 89 98",
        "email": COMPANY["email"],
        "priceRange": "270–330 kr/h",
        "address": {"@type": "PostalAddress", "streetAddress": COMPANY["street"],
                    "postalCode": COMPANY["zip"], "addressLocality": COMPANY["city"], "addressCountry": "SE"},
        "areaServed": ["Hisingen", "Kärra", "Göteborg"],
        "sameAs": [COMPANY["facebook"], COMPANY["instagram"]],
    }


def breadcrumbs(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Hem", "item": SITE_URL + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE_URL + path}]}


def offer_section(selected=None):
    return f"""<section class="section offer" id="offert">
  <div class="wrap offer-grid">
    <div class="offer-copy">
      <p class="kicker">Kostnadsfri offert</p>
      <h2>Berätta vad du behöver – vi återkommer med ett pris.</h2>
      <p class="lede">Två korta steg. Inte bindande.</p>
      <ul class="contact-cards">
        <li><a href="{COMPANY['phone_href']}"><span class="cc-icon">{icon('phone')}</span><span><small>Ring oss</small><strong>{COMPANY['phone']}</strong></span></a></li>
        <li><a href="mailto:{COMPANY['email']}"><span class="cc-icon">{icon('mail')}</span><span><small>Mejla oss</small><strong>{COMPANY['email']}</strong></span></a></li>
        <li><a href="{COMPANY['maps']}" rel="noopener"><span class="cc-icon">{icon('pin')}</span><span><small>Besök oss</small><strong>{COMPANY['street']}, {COMPANY['city']}</strong></span></a></li>
      </ul>
    </div>
    {quote_form(selected)}
  </div>
</section>"""


# --------------------------------------------------------------------- pages

def home():
    price_rows = "".join(
        f"<tr><th scope=row><a href='/{s['slug']}/'>{s['name']}</a></th>"
        f"<td>{price_label(s)}</td>"
        f"<td>{(str(s['kvm']) + chr(160) + 'kr/kvm') if s['kvm'] else '–'}</td>"
        f"<td>{'ex. moms' if s['business'] else 'efter RUT, inkl. moms'}</td></tr>"
        for s in SERVICES)

    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

    body = f"""
<section class="hero">
  {picture('home', 'Städare från Kärra Hemstäd torkar av en yta', '100vw', 'hero-img', eager=True, pos='65% center')}
  <div class="wrap hero-inner">
    <p class="kicker kicker-light">Kärra Hemstäd · Hisingen &amp; Göteborg</p>
    <h1>Professionell städning för hem och företag.</h1>
    <p class="lede">Hemstädning från 275&nbsp;kr/h efter RUT. Kollektivavtal, ansvarsförsäkring och kvalitetsgaranti – med samma städare varje gång.</p>
    <div class="cta-row">
      <a class="btn btn-primary btn-xl" href="#offert" data-quote>Begär kostnadsfri offert {icon('arrow')}</a>
      <a class="btn btn-outline-light btn-xl" href="{COMPANY['phone_href']}">{icon('phone')} {COMPANY['phone']}</a>
    </div>
  </div>
  <a class="hero-scroll" href="#rakna" aria-label="Till priskalkylatorn">{icon('down')}</a>
</section>

<section class="calc-wrap" id="rakna">
  <div class="wrap">{calculator()}</div>
</section>

<section class="section section-tight">
  <div class="wrap">{facts_band()}</div>
</section>

<section class="section section-alt" id="tjanster">
  <div class="wrap">
    <div class="head-row">
      {section_head('Våra tjänster', 'Städning för alla behov')}
      <p class="head-aside">För privatpersoner, bostadsrättsföreningar och företag. Klicka på en tjänst för att se exakt vad som ingår.</p>
    </div>
    <ul class="cards">{''.join(service_card(s) for s in SERVICES)}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="audience">
      <a class="aud" href="/hemstadning/">
        {picture('hemstad', '', '(min-width: 900px) 50vw, 100vw', 'cover')}
        <span class="aud-body">
          <span class="kicker kicker-light">Privat</span>
          <span class="aud-title">För ditt hem</span>
          <span class="aud-text">Hemstädning, flyttstädning, storstädning, fönsterputs och dödsbo. Priser efter RUT med material.</span>
          <span class="btn btn-primary">Se tjänster för hemmet {icon('arrow')}</span>
        </span>
      </a>
      <a class="aud" href="/kontorstadning/">
        {picture('kontorstad', '', '(min-width: 900px) 50vw, 100vw', 'cover')}
        <span class="aud-body">
          <span class="kicker kicker-light">Företag &amp; föreningar</span>
          <span class="aud-title">För er verksamhet</span>
          <span class="aud-text">Kontorsstädning, trappstädning och industristädning. Upplägg och pris efter era lokaler.</span>
          <span class="btn btn-primary">Se företagstjänster {icon('arrow')}</span>
        </span>
      </a>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap split">
    <div class="split-media">{picture('storstad', 'Städare torkar av en vägg', '(min-width: 900px) 50vw, 100vw', 'cover', pos='68% center')}
      <div class="split-badge"><strong>100&nbsp;%</strong><span>nöjd kund-garanti</span></div>
    </div>
    <div class="split-copy">
      {section_head('Varför Kärra Hemstäd', 'Ett lokalt städbolag med ordning och reda.')}
      {guarantees_block()}
    </div>
  </div>
</section>

<section class="section section-navy">
  <div class="wrap">
    {section_head('Så går det till', 'Från förfrågan till skinande rent', center=True, light=True)}
    <ol class="steps">
      <li><span class="step-n">01</span><h3>Du får ett pris</h3><p>Räkna själv i kalkylatorn eller skicka en förfrågan. Vi bekräftar priset innan något bokas.</p></li>
      <li><span class="step-n">02</span><h3>Vi går igenom uppdraget</h3><p>Första gången skriver vi tillsammans ner vad som ska göras. Det blir vårt protokoll.</p></li>
      <li><span class="step-n">03</span><h3>Vi städar, du godkänner</h3><p>Är något inte bra gör vi om det utan kostnad. Garantin gäller tills du har godkänt.</p></li>
    </ol>
  </div>
</section>

<section class="feature" id="flyttjanst">
  {picture('flytt', 'Flyttpersonal lastar ur kartonger ur en flyttbil', '100vw', 'feature-img')}
  <div class="wrap feature-inner">
    <div class="feature-card">
      <p class="kicker">Flytthjälp</p>
      <h2>{MOVING['title']}</h2>
      {''.join(f'<p>{p}</p>' for p in MOVING['body'])}
      <ul class="checks">
        <li>{icon('check')}<span>Packning, bärhjälp och transport</span></li>
        <li>{icon('check')}<span>Flyttstädning från {BY_SLUG['flyttstadning']['kvm']}&nbsp;kr/kvm efter RUT</span></li>
        <li>{icon('check')}<span>Bortforsling av det du inte vill ta med</span></li>
      </ul>
      <div class="cta-row">
        <a class="btn btn-primary btn-lg" href="#offert" data-quote data-service="flytthjalp">Offert på flytt {icon('arrow')}</a>
        <a class="btn btn-link" href="/flyttstadning/">Om flyttstädning</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="priser">
  <div class="wrap price-grid">
    <div>
      {section_head('Priser och RUT', 'Öppna priser. RUT redan avdraget.', 'Som privatperson betalar du halva arbetskostnaden – vi drar av resten direkt på fakturan. Avdraget är 50&nbsp;% upp till 75&nbsp;000&nbsp;kr per person och år.')}
      <div class="example"><span class="label">Exempel</span><p>Flyttstädning av en tvåa på 60&nbsp;kvm<br><strong>60 × 40&nbsp;kr = 2&nbsp;400&nbsp;kr</strong> efter RUT, material ingår.</p></div>
      <p class="small"><a href="https://www.skatteverket.se/foretagorganisationer/skatter/rotrutarbete.4.2ef18e6a125660db8b080002674.html" rel="noopener">Läs mer om RUT hos Skatteverket</a></p>
    </div>
    <div class="table-wrap">
      <table class="prices">
        <thead><tr><th scope="col">Tjänst</th><th scope="col">Pris</th><th scope="col">Per kvm</th><th scope="col"></th></tr></thead>
        <tbody>{price_rows}</tbody>
      </table>
      <p class="small muted">Privatpriser inkl. moms efter RUT. Företagspriser ex. moms. Industri- och trappstädning: fast pris efter genomgång.</p>
    </div>
  </div>
</section>

<section class="section section-alt" id="fragor">
  <div class="wrap faq-grid">
    <div>
      {section_head('Vanliga frågor', 'Bra att veta', f'Hittar du inte svaret? Ring <a href="{COMPANY["phone_href"]}">{COMPANY["phone"]}</a>.')}
    </div>
    {faq_block(FAQ)}
  </div>
</section>

{offer_section()}
"""
    return page("Städfirma i Göteborg & på Hisingen – hemstädning från 275 kr/h | Kärra Hemstäd",
                "Professionell städning för hem och företag på Hisingen och i Göteborg. Hemstädning, flyttstädning, storstädning, kontor och trapphus. Kollektivavtal, försäkring och kvalitetsgaranti.",
                "/", body, jsonld=[local_business(), faq_ld])


def service_page(s):
    groups = "".join(f'<div class="inc-group"><h3>{t}</h3>{checklist(items)}</div>' for t, items in s["included"])
    notes = "".join(f'<div class="note"><h3>{t}</h3><p>{n}</p></div>' for t, n in s["notes"])
    docs = ""
    if s["docs"]:
        docs = '<div class="docs"><h3>Ladda ner</h3><ul>' + "".join(
            f'<li><a href="/{DOCS[d][1]}">{icon("file")}{DOCS[d][0]} <small>PDF</small></a></li>' for d in s["docs"]) + "</ul></div>"
    if s.get("price_note"):
        detail = s["price_note"]
    else:
        detail = "ex. moms" if s["business"] else "efter RUT, inkl. moms och material"
        if s["kvm"]:
            ex = 70 if not s["business"] else 200
            detail += f' · eller {s["kvm"]}&nbsp;kr/kvm ({ex}&nbsp;kvm = {kr(ex * s["kvm"])})'
    extra = f"""<div class="banner-price"><strong>{price_head(s)}</strong><span>{detail}</span></div>
    <div class="cta-row">
      <a class="btn btn-primary btn-xl" href="#offert" data-quote>Begär offert {icon('arrow')}</a>
      <a class="btn btn-outline-light btn-xl" href="{COMPANY['phone_href']}">{icon('phone')} {COMPANY['phone']}</a>
    </div>"""
    others = "".join(service_card(o) for o in SERVICES if o["slug"] != s["slug"])
    path = f"/{s['slug']}/"
    group_name = "Företag" if s["business"] else "Privat"
    service_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["name"],
                  "serviceType": s["name"], "provider": {"@id": SITE_URL + "/#company"},
                  "areaServed": ["Hisingen", "Göteborg"]}

    body = f"""
{banner(s['img'], group_name, s['name'], s['lead'], [('Tjänster', '/#tjanster'), (s['name'], None)], extra, pos=s.get('img_pos'))}

<section class="section section-tight">
  <div class="wrap">{facts_band()}</div>
</section>

<section class="section section-alt">
  <div class="wrap content-grid">
    <div class="content">
      <div class="prose">{''.join(f'<p>{p}</p>' for p in s['intro'])}</div>
      <h2 class="h-inc">Det här ingår</h2>
      <div class="inc">{groups}</div>
      {notes}
      {docs}
    </div>
    <aside class="aside" id="offert">
      {quote_form(s['slug'], f"Offert på {s['name'].lower()}", compact=True)}
    </aside>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head('Fler tjänster', 'Vi hjälper dig även med')}
    <ul class="cards cards-scroll">{others}</ul>
  </div>
</section>
"""
    ph = price_head(s).replace('&nbsp;', ' ')
    title = f"{s['name']} i Göteborg & på Hisingen – {ph} | Kärra Hemstäd"
    desc = f"{s['name']} från Kärra Hemstäd. {s['lead']} {ph} {price_suffix(s)}. Kollektivavtal, försäkring och kvalitetsgaranti."
    return page(title, desc, path, body, active=s["slug"], jsonld=[service_ld, breadcrumbs(s["name"], path)])


def about_page():
    secs = "".join(f'<div class="about-item"><h3>{t}</h3><p>{p}</p></div>' for t, p in ABOUT["sections"])
    body = f"""
{banner('home', 'Om oss', 'Det lokala städbolaget i Kärra.', ABOUT['intro'], [('Om oss', None)], pos='65% center')}
<section class="section">
  <div class="wrap split">
    <div class="split-media">{picture('hemstad', 'Ett nystädat vardagsrum', '(min-width: 900px) 50vw, 100vw', 'cover')}</div>
    <div class="split-copy">
      {section_head('Vilka vi är', 'Det lilla företaget med det stora drivet.')}
      <div class="about-list">{secs}</div>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    {section_head('Våra löften', 'Det här gäller alltid, oavsett uppdrag.')}
    {guarantees_block()}
  </div>
</section>
{offer_section()}
"""
    return page("Om oss | Kärra Hemstäd – lokal städfirma på Hisingen",
                "Kärra Hemstäd är ett lokalt städbolag i Kärra med utbildad personal, kollektivavtal och ansvarsförsäkring. Samma städare varje gång.",
                "/om-oss/", body, active="om-oss", jsonld=[local_business(), breadcrumbs("Om oss", "/om-oss/")])


def contact_page():
    body = f"""
{banner('kontorstad', 'Kontakt', 'Kontakta oss', 'Har du frågor eller vill boka? Ring, mejla eller skicka en förfrågan så hör vi av oss så snart vi kan.', [('Kontakt', None)])}
{offer_section()}
<section class="section section-alt section-tight">
  <div class="wrap">
    <dl class="contact-dl">
      <div><dt>Företag</dt><dd>{COMPANY['legal']}</dd></div>
      <div><dt>Adress</dt><dd><a href="{COMPANY['maps']}" rel="noopener">{COMPANY['street']}, {COMPANY['zip']} {COMPANY['city']}</a></dd></div>
      <div><dt>Område</dt><dd>{COMPANY['area']}</dd></div>
    </dl>
  </div>
</section>
"""
    return page("Kontakta oss | Kärra Hemstäd", f"Ring {COMPANY['phone']} eller mejla {COMPANY['email']}. Kärra Hemstäd AB, {COMPANY['street']}, {COMPANY['city']}.",
                "/kontakta-oss/", body, active="kontakta-oss", jsonld=[local_business(), breadcrumbs("Kontakt", "/kontakta-oss/")])


def not_found():
    body = f"""
<section class="section plain-hero">
  <div class="wrap">
    <p class="kicker">404</p>
    <h1>Sidan finns inte.</h1>
    <p class="lede">Den kan ha flyttats när vi byggde om sajten. Börja på <a href="/">startsidan</a> eller ring <a href="{COMPANY['phone_href']}">{COMPANY['phone']}</a>.</p>
  </div>
</section>"""
    return page("Sidan hittades inte | Kärra Hemstäd", "Sidan finns inte.", "/404.html", body, overlay=False)


# --------------------------------------------------------------------- assets

def build_images():
    src = SRC / "assets" / "img"
    dst = OUT / "assets" / "img"
    dst.mkdir(parents=True, exist_ok=True)
    for s in {s["img"] for s in SERVICES} | {"flytt", "home"}:
        im = Image.open(src / f"{s}.jpg").convert("RGB")
        for w in (640, 1200, 1920):
            h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).save(dst / f"{s}-{w}.webp", "WEBP", quality=74, method=6)
    og = Image.open(src / "home.jpg").convert("RGB")
    og = og.resize((1200, round(og.height * 1200 / og.width)), Image.LANCZOS)
    top = (og.height - 630) // 2
    og.crop((0, top, 1200, top + 630)).save(dst / "og.jpg", "JPEG", quality=82, optimize=True)
    shutil.copy(src / "logo-web.png", dst / "logo.png")
    for size in (32, 180, 192):
        shutil.copy(src / f"cropped-512-1-{size}x{size}.png", dst / f"icon-{size}.png")
    docs = OUT / "assets" / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    shutil.copy(SRC / "assets" / "docs" / "NYCKELKVITTENS2024.pdf", docs / "nyckelkvittens.pdf")
    shutil.copy(SRC / "assets" / "docs" / "checklista.pdf", docs / "checklista-flyttstadning.pdf")


def write(path, html):
    p = OUT / path.strip("/") / "index.html" if not path.endswith(".html") else OUT / path.strip("/")
    p.parent.mkdir(parents=True, exist_ok=True)
    if BASE != "/":
        html = (html.replace('="/', f'="{BASE}').replace("='/", f"='{BASE}")
                .replace(", /assets/", f", {BASE}assets/")
                .replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1))
    p.write_text(html, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    build_images()
    for folder in ("css", "js"):
        shutil.copytree(SRC / folder, OUT / "assets" / folder)
    if BASE != "/":
        js = OUT / "assets" / "js" / "main.js"
        js.write_text(js.read_text(encoding="utf-8").replace('"/#offert"', f'"{BASE}#offert"'), encoding="utf-8")
    write("/", home())
    for s in SERVICES:
        write(f"/{s['slug']}/", service_page(s))
    write("/om-oss/", about_page())
    write("/kontakta-oss/", contact_page())
    write("/404.html", not_found())

    urls = ["/"] + [f"/{s['slug']}/" for s in SERVICES] + ["/om-oss/", "/kontakta-oss/"]
    today = date.today().isoformat()
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE_URL}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
        + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    # Old WordPress URLs that no longer exist (Netlify / Cloudflare Pages format).
    (OUT / "_redirects").write_text(
        "/sitemap_index.xml /sitemap.xml 301\n"
        "/wp-content/uploads/2024/02/NYCKELKVITTENS2024.pdf /assets/docs/nyckelkvittens.pdf 301\n"
        "/wp-content/uploads/2024/02/checklista.pdf /assets/docs/checklista-flyttstadning.pdf 301\n",
        encoding="utf-8")
    print(f"Built {len(urls) + 1} pages into {OUT}")


if __name__ == "__main__":
    main()
