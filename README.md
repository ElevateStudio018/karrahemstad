# karrahemstad.se

Statisk sajt för Kärra Hemstäd (Poppins, navy/cyan, helskärms-hero). Ersätter den gamla WordPress-sajten – allt innehåll, priser, bilder och PDF:er är hämtade därifrån.

## Struktur

- `src/content.py` – alla texter, priser och kontaktuppgifter. Ändra här.
- `src/build.py` – bygger sidorna och optimerar bilderna till `public/`.
- `src/css/`, `src/js/` – stil och skript (inga ramverk, inga beroenden utöver Pillow för bildbygget).
- `src/assets/` – originalbilder, logga och PDF:er från gamla sajten.
- `public/` – färdig sajt. Det är den här mappen som publiceras.

## Bygga

```sh
pip install pillow
python3 src/build.py
python3 -m http.server -d public 8000   # förhandsgranska på http://localhost:8000
```

## Publicera

`public/` kan läggas på valfritt statiskt webbhotell (Netlify, Cloudflare Pages, GitHub Pages, vanligt webbhotell).
`public/_redirects` pekar gamla WordPress-PDF-länkar till de nya adresserna (Netlify/Cloudflare-format).
Sidornas adresser (`/hemstadning/`, `/flyttstadning/` osv.) är desamma som förut, så befintliga Google-länkar fungerar.

## Offertformuläret

Sätt `FORM_ENDPOINT` i `src/content.py` till en formulärtjänst som tar emot JSON (t.ex. Formspree eller Web3Forms) och bygg om.
Så länge den är tom öppnar formuläret ett färdigifyllt mejl till info@karrahemstad.se.

## Förhandsvisning på GitHub Pages

`preview/` är samma sajt byggd för adressen https://elevatestudio018.github.io/karrahemstad/preview/ (med `noindex`).
Bygg om den efter ändringar:

```sh
BASE_PATH=/karrahemstad/preview/ OUT_DIR=preview python3 src/build.py
```
