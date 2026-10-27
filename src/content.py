"""All site copy and prices, taken from the old karrahemstad.se (scraped 2026-10-27).

Change prices and texts here, then run `python3 src/build.py`.
"""

COMPANY = {
    "name": "Kärra Hemstäd",
    "legal": "Kärra Hemstäd AB",
    "phone": "031-27 89 98",
    "phone_href": "tel:+4631278998",
    "email": "info@karrahemstad.se",
    "street": "Litteraturgatan 146",
    "zip": "422 63",
    "city": "Hisings Backa",
    "maps": "https://www.google.com/maps/search/?api=1&query=Litteraturgatan+146,+422+63+Hisings+Backa",
    "facebook": "https://www.facebook.com/karrahemstad/",
    "instagram": "https://www.instagram.com/karrahemstad/",
    "area": "Hisingen, Kärra och Göteborg med omnejd",
}

SITE_URL = "https://karrahemstad.se"

# Where quote forms are POSTed (JSON). Works with e.g. Formspree or Web3Forms.
# Leave empty and the form opens a pre-filled e-mail to COMPANY["email"] instead.
FORM_ENDPOINT = ""

PROPERTY_PRIVATE = ["Lägenhet", "Radhus", "Hus", "Fritidshus"]
PROPERTY_BUSINESS = ["Kontor", "Butik", "Restaurang", "Industri/Lager"]

# kvm = price per square metre, hour = price per hour (from the old calculator).
# business=True: prices are ex. moms. Otherwise incl. moms after RUT.
SERVICES = [
    {
        "slug": "hemstadning",
        "name": "Hemstädning",
        "lead": "Återkommande städning av ditt hem – samma städare varje gång.",
        "hour": 275,
        "kvm": 25,
        "img": "hemstad",
        "business": False,
        "intro": [
            "Känslan av att komma hem till ett nystädat hem efter en lång arbetsdag är svår att slå. "
            "Tiden du vinner kan du lägga på familj, vänner – eller på att inte göra någonting alls.",
            "Vid första besöket går vi igenom hemmet tillsammans och skriver ner vad som ska göras, "
            "även hur vi hanterar ömtåliga saker som bokhyllor och vitrinskåp. Sedan följer vi protokollet varje gång.",
        ],
        "included": [
            ("Kök och matrum", [
                "Kyl, frys och skåpsluckor rengörs utvändigt",
                "Spis och fläktkåpa rengörs",
                "Diskbänk och vask rengörs (fria från föremål och disk)",
                "Fönsterbrädor, bord och stolar dammas av",
                "Golvet rengörs",
            ]),
            ("Badrum och WC", [
                "Handfat och toalett rengörs",
                "Speglar putsas",
                "Badkar och/eller duschkabin torkas av",
                "Gallret till golvbrunnen rengörs",
                "Kakel putsas rent",
                "Golvet rengörs",
            ]),
            ("Vardagsrum och sovrum", [
                "Dammtorkning av öppna, fria ytor",
                "Golven rengörs",
            ]),
        ],
        "notes": [],
        "docs": ["nyckel"],
        "property": PROPERTY_PRIVATE,
    },
    {
        "slug": "flyttstadning",
        "name": "Flyttstädning",
        "lead": "Vi städar ur din gamla bostad så att du kan fokusera på den nya.",
        "hour": 297,
        "kvm": 40,
        "img": "flyttstad",
        "business": False,
        "intro": [
            "Att flytta är stressigt. Du ska planera, packa, frakta allt till rätt plats – och dessutom "
            "städa ur det gamla hemmet. Lämna flyttstädningen till oss och lägg tiden på det nya hemmet istället.",
            "Vi utför flyttstädningen med försäkring och kvalitetsgaranti. Behöver du hjälp med själva flytten också "
            "tar vi hand om den.",
        ],
        "included": [
            ("Kök", [
                "Köksskåp och lådor in- och utvändigt",
                "Kyl, sval och frys in- och utvändigt samt bakom",
                "Spis, spisplattor, ugn och ugnsplåtar – in- och utvändigt, bakom och under",
                "Diskmaskin in- och utvändigt, bakom och under",
                "Kakel och väggar",
                "Fönsterputs och fönsterkarmar",
                "Dörrar, dörrfoder, lister, fönsterbrädor, kontakter och element",
                "Dammsugning och våttorkning av golv",
                "Avtorkning av belysning",
                "Sopor",
            ]),
            ("Badrum", [
                "WC-stol och handfat",
                "Badkar och duschkabin in- och utvändigt",
                "Alla avlopp och rör",
                "Dörrar, karmar och handtag",
                "Lister, väggar, tak och golv",
                "Skåp och badrumsskåp in- och utvändigt",
                "Tvättmaskin och torktumlare",
                "Sopor",
            ]),
            ("Boyta", [
                "Luftintag och ventiler",
                "Golvlister, kontakter, dörrar, dörrkarmar, element och fönsterbrädor",
                "Garderober och övriga skåp in- och utvändigt",
                "Fönsterputs och fönsterkarmar",
                "Sopor",
            ]),
            ("Övriga utrymmen", [
                "Garage",
                "Tvättstuga",
                "Förråd",
                "Övrigt enligt överenskommelse",
            ]),
        ],
        "notes": [
            ("Inför flyttstädningen",
             "Töm kyl och frys, stäng av dem och se till att frysen är avfrostad när vi börjar. "
             "Har du saker som ska forslas bort – säg till någon dag innan så att vi kan ordna transport. "
             "Berätta också om något är trasigt eller kräver särskild rengöring, till exempel självrengörande ugn eller fönster."),
        ],
        "docs": ["checklista", "nyckel"],
        "property": PROPERTY_PRIVATE + PROPERTY_BUSINESS,
    },
    {
        "slug": "storstadning",
        "name": "Storstädning",
        "lead": "Grundlig städning av hela bostaden – inför våren, högtider eller en visning.",
        "hour": 297,
        "kvm": 27,
        "img": "storstad",
        "business": False,
        "intro": [
            "En storstädning går på djupet: insidan av skåp, bakom vitvaror, lister, ventiler och kakel. "
            "Det som inte hinns med i vardagen.",
            "Vid första besöket går vi igenom vad som ska göras och hur vi hanterar ömtåliga saker. "
            "Allt vi kommer överens om skrivs ner.",
        ],
        "included": [
            ("Bostadsrum", [
                "Rengöring av golv",
                "Golvlister, kontakter, dörrar, karmar, fönsterbrädor och element",
                "Garderober in- och utvändigt (om de är tömda)",
            ]),
            ("Kök", [
                "Kyl, sval och frys in- och utvändigt samt under (frysen avfrostad)",
                "Utdragen spis in- och utvändigt, även ugnsplåtar",
                "Skåp, lådor och bänkar in- och utvändigt (om de är tömda)",
                "Köksfläkt och ventiler (utvändigt)",
                "Avtorkning av belysning",
            ]),
            ("Bad och toalett", [
                "All sanitet, även under badkaret",
                "Kakelväggar",
                "Tvättmaskin, torktumlare och torkskåp in- och utvändigt",
                "Golvbrunnar och ventiler",
                "Förvaringsutrymmen",
                "Avtorkning av belysning",
            ]),
        ],
        "notes": [],
        "docs": ["nyckel"],
        "property": PROPERTY_PRIVATE + PROPERTY_BUSINESS,
    },
    {
        "slug": "fonsterputsning",
        "name": "Fönsterputsning",
        "lead": "Rena fönster in- och utsida, även på övervåningen.",
        "hour": 270,
        "kvm": None,
        "img": "fonsterputs",
        "price_label": "70 kr/fönster",
        "price_note": "med hemstädning som abonnemang. Enstaka fönsterputs utan hemstädning: 90 kr/fönster.",
        "img_pos": "left center",
        "business": False,
        "intro": [
            "Solen tittar fram och genast syns det hur dammiga fönstren blivit. Många drar sig för fönsterputsen – "
            "särskilt fönstren på övervåningen som inte går att öppna inåt.",
            "Vi putsar in- och utsida, mellan glasen om fönstren är delbara, och torkar upp efter oss.",
        ],
        "included": [
            ("Fönster", [
                "Putsning in- och utsida",
                "Mellan glasen om du har delbara fönster",
                "Rengöring av spröjs",
                "Borttagning och montering av löstagbara spröjs",
                "Vi torkar bort eventuellt spill efter oss",
            ]),
        ],
        "notes": [],
        "docs": ["nyckel"],
        "property": PROPERTY_PRIVATE + PROPERTY_BUSINESS,
    },
    {
        "slug": "dodsbostadning",
        "name": "Dödsbostädning",
        "lead": "Tömning och städning av dödsbo, varsamt och utan stress för de anhöriga.",
        "hour": 270,
        "kvm": 27,
        "img": "dodsbostad",
        "business": False,
        "intro": [
            "Att tömma ett dödsbo är en stor uppgift – inte bara praktiskt utan också känslomässigt. "
            "Vi tömmer bostaden på allt som ska bort och städar efteråt.",
            "Vi samarbetar med flera hjälporganisationer och lämnar gärna saker till dem om ni vill. "
            "Annars sorteras allt och lämnas på närmaste återvinningsstation.",
        ],
        "included": [
            ("Bostadsrum", [
                "Rengöring av golv",
                "Golvlister, kontakter, dörrar, karmar, fönsterbrädor och element",
                "Garderober in- och utvändigt (om de är tömda)",
            ]),
            ("Kök", [
                "Kyl, sval och frys in- och utvändigt samt under (frysen avfrostad)",
                "Utdragen spis in- och utvändigt, även ugnsplåtar",
                "Skåp, lådor och bänkar in- och utvändigt",
                "Köksfläkt och ventiler (utvändigt)",
                "Avtorkning av belysning",
            ]),
            ("Bad och toalett", [
                "All sanitet, även under badkaret",
                "Kakelväggar",
                "Tvättmaskin, torktumlare och torkskåp in- och utvändigt",
                "Golvbrunnar och ventiler",
                "Förvaringsutrymmen",
                "Avtorkning av belysning",
            ]),
        ],
        "notes": [],
        "docs": ["nyckel"],
        "property": PROPERTY_PRIVATE,
    },
    {
        "slug": "kontorstadning",
        "name": "Kontorstädning",
        "lead": "Ett rent kontor när ni tänder lampan på morgonen.",
        "hour": 330,
        "kvm": 30,
        "img": "kontorstad",
        "business": True,
        "intro": [
            "Vi städar efter att ni gått hem, så att kontoret är klart när ni kommer tillbaka. "
            "Upplägget anpassas efter era lokaler och hur ofta ni behöver städning.",
            "Samma personal kommer varje gång och alla bär ID-kort med foto.",
        ],
        "included": [
            ("Samtliga rum", [
                "Dammsugning av golv och mattor",
                "Fuktmoppning av golv",
                "Damning av fria ytor",
                "Fläckar tas bort på speglar, lister och dörrar",
                "Tömning av papperskorgar",
            ]),
            ("Toaletter", [
                "Handfat och toalett rengörs in- och utvändigt",
            ]),
            ("Kök och pentry", [
                "Rengöring av kök eller pentry",
                "Avtorkning av arbetsbänk och diskbänk",
            ]),
        ],
        "notes": [],
        "docs": [],
        "property": PROPERTY_BUSINESS,
    },
    {
        "slug": "trappstadning",
        "name": "Trappstädning",
        "lead": "För bostadsrättsföreningar och hyresvärdar.",
        "hour": 280,
        "kvm": None,
        "img": "trappstad",
        "business": True,
        "intro": [
            "Ett rent trapphus höjer trivseln och minskar risken för halkolyckor, klotter och onödigt slitage. "
            "Vi städar trapphus åt bostadsrättsföreningar och hyresvärdar.",
            "Vi använder miljövänliga medel och egna redskap. Ni ger oss tillgång till lokalerna – vi sköter resten.",
        ],
        "included": [
            ("Trapphus", [
                "Sopning och fuktmoppning",
                "Dammtorkning av fönsterkarmar och trappräcken",
                "Ledstänger",
                "Fönsterputs",
                "Rengöring av tvättstugor",
                "Dörrmattor skakas och golvet under sopas",
            ]),
        ],
        "notes": [],
        "docs": [],
        "property": ["Bostadsrättsförening", "Hyresfastighet"] + PROPERTY_BUSINESS,
    },
    {
        "slug": "industristadning",
        "name": "Industristädning",
        "lead": "Verkstäder, lager och produktion – med rätt utrustning.",
        "hour": 280,
        "kvm": 28,
        "img": "industristad",
        "business": True,
        "intro": [
            "Maskiner och arbetsytor i industrier, verkstäder och lager ställer andra krav än ett kontor – "
            "på personalen, på utförandet och på utrustningen.",
            "Kontakta oss för en genomgång av era lokaler så får ni ett upplägg och ett pris som passar verksamheten.",
        ],
        "included": [
            ("Känsliga miljöer", [
                "Dammsugning av öppna, fria och vertikala ytor",
                "Avtorkning av belysning, lister, dörrfoder, dörrar och element",
                "Avfläckning av väggar",
                "Dammsugning och våttorkning av golv och horisontella ytor",
                "Golvbehandling, t.ex. vaxning eller polering med antistatisk polish",
                "Specialstädning av elektronisk utrustning med isblästring",
            ]),
            ("Industri och lager", [
                "Städning av samtliga arbetsområden",
                "Mekanisk skurning med högtryckstvätt av golv",
                "Golvvård med skur- och sopmaskin",
                "Dammtorkning av fria ytor",
                "Grovstädning och avfettning av maskiner",
                "Tömning av avfallstunnor",
                "Rengöring av garage",
            ]),
            ("Verkstäder", [
                "Städning av omklädningsrum",
                "Dammsugning av golv och väggar",
                "Verkstadsgolv med sop- och skurmaskin",
                "Grovstädning och avfettning av maskiner",
                "Avtorkning av belysning",
            ]),
        ],
        "notes": [],
        "docs": [],
        "property": PROPERTY_BUSINESS,
    },
]

DOCS = {
    "nyckel": ("Nyckelkvittens", "assets/docs/nyckelkvittens.pdf"),
    "checklista": ("Checklista för flyttstädning", "assets/docs/checklista-flyttstadning.pdf"),
}

GUARANTEES = [
    ("Kvalitetsgaranti",
     "Garantin gäller tills du har godkänt städningen. Är något inte bra gör vi om det utan kostnad."),
    ("Ansvarsförsäkring",
     "Fullt försäkringsskydd för skador på person och egendom som vår personal orsakar."),
    ("Kollektivavtal",
     "Vår personal har ordnade villkor. Det ska kännas bra hela vägen."),
    ("Samma städare varje gång",
     "Du vet vem som kommer. All personal är kontrollerad mot belastningsregistret och bär ID-kort med foto."),
    ("Miljömärkta medel ingår",
     "Vi tar med städmaterial och använder miljömärkta produkter. Det ingår i priset."),
]

FAQ = [
    ("Hur fungerar RUT-avdraget?",
     "Som privatperson betalar du bara halva arbetskostnaden – resten drar vi av direkt på fakturan och begär från Skatteverket. "
     "Avdraget är 50 % av arbetskostnaden, upp till 75 000 kr per person och år. "
     "Priserna för privatpersoner på sajten är redan räknade efter RUT och inklusive moms och material."),
    ("Vad händer om jag inte är nöjd?",
     "Säg till innan du godkänner städningen, så åtgärdar vi det utan extra kostnad. "
     "Garantin gäller tills du har godkänt städningen."),
    ("Kommer samma person varje gång?",
     "Ja. Du får samma städare vid varje tillfälle. All personal är kontrollerad mot belastningsregistret och bär ID-kort med foto."),
    ("Måste jag vara hemma?",
     "Nej. Många kunder lämnar en nyckel. Vi skriver då en nyckelkvittens – du kan ladda ner den i förväg."),
    ("Behöver jag ta fram städmaterial?",
     "Nej, vi tar med allt. Miljömärkta städmedel ingår i priset."),
    ("Var utför ni städning?",
     "Vi utgår från Kärra och städar på hela Hisingen och i Göteborg med omnejd. Osäker på om vi kommer till dig? Ring oss."),
    ("Vad ska jag tänka på inför flyttstädningen?",
     "Töm kyl och frys, stäng av dem och frosta av frysen innan vi kommer. "
     "Säg också till om något är trasigt eller kräver särskild rengöring."),
]

MOVING = {
    "title": "Flytthjälp och flyttstädning – i samma bokning",
    "body": [
        "Vi tar hand om både flytten och flyttstädningen, så att du kan lägga energin på ditt nya hem eller kontor.",
        "Vi har hjälpt många privatpersoner och företag genom åren – från packning och bärhjälp till nyckelöverlämning efter flyttstädningen.",
    ],
}

ABOUT = {
    "intro": "Kärra Hemstäd har hjälpt hundratals kunder på Hisingen. Vi är ett litet, effektivt team med utbildad personal – "
             "och vi städar både hem och små och medelstora företag.",
    "sections": [
        ("Vilka vi är",
         "Ett litet företag med gedigen kunskap om städning. Det lilla företaget med det stora drivet. "
         "Vi vill att alla kunder ska vara nöjda, därför har vi kvalitetsgaranti på allt vi gör."),
        ("Vår personal",
         "Det är alltid samma personal som städar hos dig. All personal genomgår en säkerhetsprövning, bland annat "
         "med utdrag ur belastningsregistret, och bär alltid ID-kort med foto. Vi har kollektivavtal och ansvarsförsäkring."),
        ("Miljön",
         "Vi använder miljövänliga medel, planerar våra transporter, sorterar vårt avfall och kräver detsamma av våra underleverantörer."),
        ("Varför vi finns",
         "Vardagen är full av jobb och familj. Vi tar hand om städningen så att du får tid över till det som är viktigt för dig."),
    ],
}
