#!/usr/bin/env python3
"""Builds the static site into public/.  Usage: python3 src/build.py"""
import json
import shutil
from datetime import date
from html import escape as e
from pathlib import Path

from PIL import Image

from content import (ABOUT, COMPANY, DOCS, FAQ, FORM_ENDPOINT, GUARANTEES, MOVING,
                     SERVICES, SITE_URL)

SRC = Path(__file__).parent
OUT = SRC.parent / "public"
ASSET_VERSION = date.today().strftime("%Y%m%d")
BY_SLUG = {s["slug"]: s for s in SERVICES}


def kr(n):
    return f"{n:,}".replace(",", " ") + " kr"


def price_label(s):
    return s.get("price_label") or f"{s['hour']} kr/h"


def price_suffix(s):
    return "ex. moms" if s["business"] else "efter RUT"


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
<meta name="theme-color" content="#f5f3ee">
<link rel="icon" href="/assets/img/icon-32.png" sizes="32x32">
<link rel="icon" href="/assets/img/icon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={ASSET_VERSION}">
<script>document.documentElement.classList.add("js")</script>
<script src="/assets/js/main.js?v={ASSET_VERSION}" defer></script>
{ld}
</head>"""


def header(active=""):
    service_links = "".join(
        f'<li><a href="/{s["slug"]}/"{" aria-current=page" if active == s["slug"] else ""}>'
        f'<span>{s["name"]}</span><small>{price_label(s)}</small></a></li>'
        for s in SERVICES)
    is_service = active in BY_SLUG

    def cur(key):
        return ' aria-current="page"' if active == key else ""

    return f"""<body>
<a class="skip" href="#main">Hoppa till innehållet</a>
<header class="site-header">
  <div class="wrap header-row">
    <a class="logo" href="/" aria-label="{COMPANY['name']} – startsidan">
      <img src="/assets/img/logo.png" alt="{COMPANY['name']}" width="180" height="40">
    </a>
    <nav class="nav" id="nav" aria-label="Huvudmeny">
      <ul class="nav-list">
        <li class="has-sub">
          <button class="nav-sub-toggle" aria-expanded="false" aria-controls="sub-services"{' data-active' if is_service else ''}>Tjänster {icon('down', 'i i-sm')}</button>
          <ul class="sub" id="sub-services">{service_links}</ul>
        </li>
        <li><a href="/#flyttjanst">Flytthjälp</a></li>
        <li><a href="/#priser">Priser</a></li>
        <li><a href="/om-oss/"{cur('om-oss')}>Om oss</a></li>
        <li><a href="/kontakta-oss/"{cur('kontakta-oss')}>Kontakt</a></li>
      </ul>
    </nav>
    <div class="header-cta">
      <a class="phone-link" href="{COMPANY['phone_href']}">{icon('phone')}<span>{COMPANY['phone']}</span></a>
      <a class="btn btn-primary btn-sm" href="#offert" data-quote>Få offert</a>
      <button class="menu-btn" aria-expanded="false" aria-controls="nav" aria-label="Meny">{icon('menu', 'i i-open')}{icon('close', 'i i-close')}</button>
    </div>
  </div>
</header>
<main id="main">"""


def footer():
    services = "".join(f'<li><a href="/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    return f"""</main>
<footer class="site-footer">
  <div class="wrap footer-top">
    <div class="footer-cta">
      <p class="h2">Frågor? Ring oss.</p>
      <a class="footer-phone" href="{COMPANY['phone_href']}">{COMPANY['phone']}</a>
      <p class="muted">Eller mejla <a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></p>
    </div>
    <div class="footer-cols">
      <div>
        <p class="footer-h">Tjänster</p>
        <ul>{services}</ul>
      </div>
      <div>
        <p class="footer-h">Företaget</p>
        <ul>
          <li><a href="/om-oss/">Om oss</a></li>
          <li><a href="/kontakta-oss/">Kontakt</a></li>
          <li><a href="/#priser">Priser och RUT</a></li>
          <li><a href="/#fragor">Vanliga frågor</a></li>
          <li><a href="/{DOCS['nyckel'][1]}">Nyckelkvittens (PDF)</a></li>
        </ul>
      </div>
      <div>
        <p class="footer-h">Besöksadress</p>
        <address>
          {COMPANY['legal']}<br>{COMPANY['street']}<br>{COMPANY['zip']} {COMPANY['city']}
        </address>
        <p class="social">
          <a href="{COMPANY['facebook']}" rel="noopener">Facebook</a>
          <a href="{COMPANY['instagram']}" rel="noopener">Instagram</a>
        </p>
      </div>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© {date.today().year} {COMPANY['legal']}</span>
    <span>Städning på {COMPANY['area']}</span>
  </div>
</footer>
<div class="mobile-bar" aria-label="Snabbkontakt">
  <a class="btn btn-ghost" href="{COMPANY['phone_href']}">{icon('phone')} Ring</a>
  <a class="btn btn-primary" href="#offert" data-quote>Få offert</a>
</div>
</body>
</html>
"""


def page(title, desc, path, body, active="", jsonld=()):
    return head(title, desc, path, jsonld) + header(active) + body + footer()


# --------------------------------------------------------------------- components

def section_head(kicker, title, text=""):
    t = f'<p class="lede">{text}</p>' if text else ""
    return f'<div class="section-head"><p class="kicker">{kicker}</p><h2>{title}</h2>{t}</div>'


def calculator(heading="Räkna på priset"):
    data = [{"slug": s["slug"], "name": s["name"], "hour": s["hour"], "kvm": s["kvm"], "business": s["business"]}
            for s in SERVICES]
    kvm_opts = "".join(f'<option value="{s["slug"]}">{s["name"]}</option>' for s in SERVICES if s["kvm"])
    return f"""<div class="calc" data-calc>
  <script type="application/json" data-calc-data>{json.dumps(data, ensure_ascii=False)}</script>
  <div class="calc-top">
    <p class="calc-title">{heading}</p>
    <div class="seg" role="radiogroup" aria-label="Räkna på">
      <label><input type="radio" name="calc-mode" value="kvm" checked><span>Per kvm</span></label>
      <label><input type="radio" name="calc-mode" value="hour"><span>Per timme</span></label>
    </div>
  </div>
  <label class="field">
    <span class="label">Tjänst</span>
    <select data-calc-service>{kvm_opts}</select>
  </label>
  <div class="field" data-calc-amount>
    <label class="label" for="calc-amount" data-calc-amount-label>Bostadens storlek</label>
    <div class="amount">
      <input id="calc-amount" type="range" min="20" max="250" step="5" value="70" data-calc-range>
      <div class="amount-num"><input type="number" inputmode="numeric" min="1" value="70" data-calc-number aria-label="Antal"><span data-calc-unit>kvm</span></div>
    </div>
  </div>
  <div class="calc-result" aria-live="polite">
    <div>
      <span class="calc-total" data-calc-total>2&nbsp;800&nbsp;kr</span>
      <span class="calc-note" data-calc-note>efter RUT, inkl. moms och material</span>
    </div>
    <a class="btn btn-primary btn-block" href="#offert" data-calc-cta>Få offert på det här {icon('arrow')}</a>
  </div>
  <p class="calc-fine">Uppskattning. Vi bekräftar alltid priset innan vi börjar.</p>
</div>"""


def quote_form(selected=None, heading="Få en offert", compact=False):
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
    <p class="quote-steps" aria-hidden="true"><span data-step-label>Steg 1 av 2</span></p>
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
    <button class="btn btn-primary btn-block" type="button" data-next>Fortsätt {icon('arrow')}</button>
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
      <button class="btn btn-ghost" type="button" data-back>Tillbaka</button>
      <button class="btn btn-primary" type="submit">Skicka förfrågan</button>
    </div>
    <p class="form-error" role="alert" data-error hidden></p>
  </fieldset>
  <div class="quote-done" data-done hidden tabindex="-1">
    <p class="quote-title">Tack! Vi hör av oss.</p>
    <p>Vi kontaktar dig så snart vi kan. Brådskande? Ring <a href="{COMPANY['phone_href']}">{COMPANY['phone']}</a>.</p>
  </div>
  <p class="quote-fine">Kostnadsfritt och inte bindande. Vi använder bara dina uppgifter för att svara dig.</p>
</form>"""


def checklist(items):
    return '<ul class="checks">' + "".join(f'<li>{icon("check")}<span>{e(i)}</span></li>' for i in items) + "</ul>"


def guarantees_block(compact=False):
    items = "".join(
        f'<li><span class="num">{i:02d}</span><div><h3>{t}</h3><p>{d}</p></div></li>'
        for i, (t, d) in enumerate(GUARANTEES, 1))
    return f'<ol class="guarantees{" guarantees-compact" if compact else ""}">{items}</ol>'


def trust_strip():
    items = ["Kollektivavtal", "Ansvarsförsäkring", "Kvalitetsgaranti", "Miljömärkta medel"]
    return '<ul class="trust">' + "".join(f'<li>{icon("check")}{t}</li>' for t in items) + "</ul>"


def faq_block(items):
    return '<div class="faq">' + "".join(
        f'<details><summary>{q}{icon("down", "i faq-i")}</summary><p>{a}</p></details>' for q, a in items) + "</div>"


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


# --------------------------------------------------------------------- pages

def home():
    rows = "".join(f"""<li><a class="svc" href="/{s['slug']}/">
  {picture(s['img'], '', '(min-width: 900px) 120px, 88px', 'svc-img', pos=s.get('img_pos'))}
  <span class="svc-text"><span class="svc-name">{s['name']}</span><span class="svc-lead">{s['lead']}</span></span>
  <span class="svc-price"><strong>{price_label(s)}</strong><small>{price_suffix(s)}</small></span>
  {icon('arrow', 'i svc-arrow')}
</a></li>""" for s in SERVICES)

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
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="kicker">Städfirma i Kärra · Hisingen</p>
      <h1>Hemstädning från 275&nbsp;kr/h. RUT och material ingår.</h1>
      <p class="lede">Lokal städfirma med kollektivavtal och kvalitetsgaranti. Samma städare varje gång – på hela Hisingen och i Göteborg.</p>
      <div class="cta-row">
        <a class="btn btn-primary btn-lg" href="#offert" data-quote>Få offert {icon('arrow')}</a>
        <a class="btn btn-ghost btn-lg" href="{COMPANY['phone_href']}">{icon('phone')} {COMPANY['phone']}</a>
      </div>
      {trust_strip()}
    </div>
    <div class="hero-calc">{calculator()}</div>
  </div>
</section>

<section class="section" id="tjanster">
  <div class="wrap">
    {section_head('Tjänster', 'Vad kan vi hjälpa dig med?', 'För privatpersoner, bostadsrättsföreningar och företag. Klicka för att se exakt vad som ingår.')}
    <ul class="svc-list">{rows}</ul>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    {section_head('Så går det till', 'Tre steg. Inga överraskningar.')}
    <ol class="steps">
      <li><span class="step-n">1</span><h3>Du får ett pris</h3><p>Räkna själv ovan eller skicka en förfrågan. Vi bekräftar priset innan något bokas.</p></li>
      <li><span class="step-n">2</span><h3>Vi går igenom hemmet</h3><p>Första gången skriver vi tillsammans ner vad som ska göras. Det blir vårt protokoll.</p></li>
      <li><span class="step-n">3</span><h3>Vi städar, du godkänner</h3><p>Är något inte bra gör vi om det utan kostnad. Garantin gäller tills du har godkänt.</p></li>
    </ol>
  </div>
</section>

<section class="section" id="flyttjanst">
  <div class="wrap split">
    <div class="split-media">{picture('flytt', 'Flyttgubbar lastar ur kartonger ur en flyttbil', '(min-width: 900px) 50vw, 100vw', 'cover')}</div>
    <div class="split-copy">
      <p class="kicker">Flytthjälp</p>
      <h2>{MOVING['title']}</h2>
      {''.join(f'<p>{p}</p>' for p in MOVING['body'])}
      <ul class="checks">
        <li>{icon('check')}<span>Packning, bärhjälp och transport</span></li>
        <li>{icon('check')}<span>Flyttstädning från {BY_SLUG['flyttstadning']['kvm']}&nbsp;kr/kvm efter RUT</span></li>
        <li>{icon('check')}<span>Bortforsling av det du inte vill ta med</span></li>
      </ul>
      <div class="cta-row">
        <a class="btn btn-primary" href="#offert" data-quote data-service="flytthjalp">Få offert på flytt {icon('arrow')}</a>
        <a class="btn btn-link" href="/flyttstadning/">Se vad flyttstädning innehåller</a>
      </div>
    </div>
  </div>
</section>

<section class="section section-dark">
  <div class="wrap">
    {section_head('Trygghet', 'Det här gäller alltid, oavsett tjänst.')}
    {guarantees_block()}
  </div>
</section>

<section class="section" id="priser">
  <div class="wrap price-grid">
    <div>
      {section_head('Priser och RUT', 'Öppna priser. RUT är redan avdraget.', 'Som privatperson betalar du halva arbetskostnaden – vi drar av resten direkt på fakturan. Avdraget är 50&nbsp;% upp till 75&nbsp;000&nbsp;kr per person och år.')}
      <p class="example"><strong>Exempel:</strong> Flyttstädning av en tvåa på 60&nbsp;kvm: 60 × 40&nbsp;kr = <strong>2&nbsp;400&nbsp;kr</strong> efter RUT, material ingår.</p>
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
    {section_head('Vanliga frågor', 'Bra att veta', f'Hittar du inte svaret? Ring <a href="{COMPANY["phone_href"]}">{COMPANY["phone"]}</a>.')}
    {faq_block(FAQ)}
  </div>
</section>

{offer_section()}
"""
    return page("Städfirma på Hisingen – hemstädning från 275 kr/h | Kärra Hemstäd",
                "Lokal städfirma i Kärra. Hemstädning, flyttstädning, storstädning och fönsterputs på Hisingen och i Göteborg. Priser efter RUT, kollektivavtal och kvalitetsgaranti.",
                "/", body, jsonld=[local_business(), faq_ld])


def offer_section(selected=None):
    return f"""<section class="section offer" id="offert">
  <div class="wrap offer-grid">
    <div class="offer-copy">
      <p class="kicker">Offert</p>
      <h2>Berätta vad du behöver – vi återkommer med ett pris.</h2>
      <p class="lede">Två korta steg. Kostnadsfritt och inte bindande.</p>
      <ul class="contact-list">
        <li>{icon('phone')}<a href="{COMPANY['phone_href']}">{COMPANY['phone']}</a></li>
        <li>{icon('mail')}<a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></li>
        <li>{icon('pin')}<a href="{COMPANY['maps']}" rel="noopener">{COMPANY['street']}, {COMPANY['city']}</a></li>
      </ul>
    </div>
    {quote_form(selected)}
  </div>
</section>"""


def service_page(s):
    groups = "".join(f'<div class="inc-group"><h3>{t}</h3>{checklist(items)}</div>' for t, items in s["included"])
    notes = "".join(f'<div class="note"><h3>{t}</h3><p>{n}</p></div>' for t, n in s["notes"])
    docs = ""
    if s["docs"]:
        docs = '<div class="docs"><h3>Ladda ner</h3><ul>' + "".join(
            f'<li><a href="/{DOCS[d][1]}">{icon("file")}{DOCS[d][0]} <small>PDF</small></a></li>' for d in s["docs"]) + "</ul></div>"
    if s.get("price_note"):
        price_detail = f'<p class="price-note">{s["price_note"]}</p>'
    else:
        lines = ["ex. moms" if s["business"] else "efter RUT, inkl. moms och material"]
        if s["kvm"]:
            ex = 70 if not s["business"] else 200
            lines.append(f'Eller {s["kvm"]}&nbsp;kr/kvm – {ex}&nbsp;kvm blir {kr(ex * s["kvm"])}')
        price_detail = "".join(f'<p class="price-note">{l}</p>' for l in lines)
    if s["business"] and s["slug"] in ("industristadning", "trappstadning"):
        price_head = f'Från {s["hour"]}&nbsp;kr/h'
    else:
        price_head = price_label(s)
    others = "".join(f'<li><a href="/{o["slug"]}/">{o["name"]} <span>{price_label(o)}</span></a></li>'
                     for o in SERVICES if o["slug"] != s["slug"])
    path = f"/{s['slug']}/"
    service_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["name"],
                  "serviceType": s["name"], "provider": {"@id": SITE_URL + "/#company"},
                  "areaServed": ["Hisingen", "Göteborg"]}

    body = f"""
<section class="page-hero">
  <div class="wrap page-hero-grid">
    <div>
      <nav class="crumbs" aria-label="Brödsmulor"><a href="/">Hem</a><span>/</span><a href="/#tjanster">Tjänster</a><span>/</span><span>{s['name']}</span></nav>
      <h1>{s['name']}</h1>
      <p class="lede">{s['lead']}</p>
      <div class="price-box">
        <p class="price-big">{price_head}</p>
        {price_detail}
      </div>
      <div class="cta-row">
        <a class="btn btn-primary btn-lg" href="#offert" data-quote>Få offert {icon('arrow')}</a>
        <a class="btn btn-ghost btn-lg" href="{COMPANY['phone_href']}">{icon('phone')} {COMPANY['phone']}</a>
      </div>
    </div>
    <div class="page-hero-media">{picture(s['img'], s['name'], '(min-width: 900px) 45vw, 100vw', 'cover', eager=True, pos=s.get('img_pos'))}</div>
  </div>
</section>

<section class="section">
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

<section class="section section-dark">
  <div class="wrap">
    {section_head('Trygghet', 'Det här gäller alltid.')}
    {guarantees_block(compact=True)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="kicker">Fler tjänster</p>
    <ul class="others">{others}</ul>
  </div>
</section>
"""
    title = f"{s['name']} på Hisingen och i Göteborg – {price_head.replace('&nbsp;', ' ')} | Kärra Hemstäd"
    desc = f"{s['name']} från Kärra Hemstäd. {s['lead']} {price_head.replace('&nbsp;', ' ')} {price_suffix(s)}. Kollektivavtal, försäkring och kvalitetsgaranti."
    return page(title, desc, path, body, active=s["slug"], jsonld=[service_ld, breadcrumbs(s["name"], path)])


def about_page():
    secs = "".join(f'<div class="about-item"><h2>{t}</h2><p>{p}</p></div>' for t, p in ABOUT["sections"])
    body = f"""
<section class="page-hero page-hero-text">
  <div class="wrap">
    <nav class="crumbs" aria-label="Brödsmulor"><a href="/">Hem</a><span>/</span><span>Om oss</span></nav>
    <h1>Det lilla städbolaget i Kärra.</h1>
    <p class="lede">{ABOUT['intro']}</p>
  </div>
</section>
<section class="section">
  <div class="wrap about-grid">{secs}</div>
</section>
<section class="section section-dark">
  <div class="wrap">
    {section_head('Trygghet', 'Våra löften till dig')}
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
<section class="page-hero page-hero-text">
  <div class="wrap contact-grid">
    <div>
      <nav class="crumbs" aria-label="Brödsmulor"><a href="/">Hem</a><span>/</span><span>Kontakt</span></nav>
      <h1>Kontakta oss</h1>
      <p class="lede">Har du frågor eller vill boka? Ring, mejla eller skicka en förfrågan så hör vi av oss så snart vi kan.</p>
      <dl class="contact-dl">
        <div><dt>Telefon</dt><dd><a class="big-link" href="{COMPANY['phone_href']}">{COMPANY['phone']}</a></dd></div>
        <div><dt>E-post</dt><dd><a class="big-link" href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></dd></div>
        <div><dt>Adress</dt><dd><a href="{COMPANY['maps']}" rel="noopener">{COMPANY['legal']}<br>{COMPANY['street']}<br>{COMPANY['zip']} {COMPANY['city']}</a></dd></div>
        <div><dt>Område</dt><dd>{COMPANY['area']}</dd></div>
      </dl>
    </div>
    <div id="offert">{quote_form(None, 'Skicka en förfrågan')}</div>
  </div>
</section>
"""
    return page("Kontakta oss | Kärra Hemstäd", f"Ring {COMPANY['phone']} eller mejla {COMPANY['email']}. Kärra Hemstäd AB, {COMPANY['street']}, {COMPANY['city']}.",
                "/kontakta-oss/", body, active="kontakta-oss", jsonld=[local_business(), breadcrumbs("Kontakt", "/kontakta-oss/")])


def not_found():
    body = f"""
<section class="page-hero page-hero-text">
  <div class="wrap">
    <h1>Sidan finns inte.</h1>
    <p class="lede">Den kan ha flyttats när vi byggde om sajten. Börja på <a href="/">startsidan</a> eller ring <a href="{COMPANY['phone_href']}">{COMPANY['phone']}</a>.</p>
  </div>
</section>"""
    return page("Sidan hittades inte | Kärra Hemstäd", "Sidan finns inte.", "/404.html", body)


# --------------------------------------------------------------------- assets

def build_images():
    src = SRC / "assets" / "img"
    dst = OUT / "assets" / "img"
    dst.mkdir(parents=True, exist_ok=True)
    for s in {s["img"] for s in SERVICES} | {"flytt"}:
        im = Image.open(src / f"{s}.jpg").convert("RGB")
        for w in (640, 1200, 1920):
            h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).save(dst / f"{s}-{w}.webp", "WEBP", quality=74, method=6)
    og = Image.open(src / "hemstad.jpg").convert("RGB")
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
    p.write_text(html, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    build_images()
    for folder in ("css", "js"):
        shutil.copytree(SRC / folder, OUT / "assets" / folder)
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
