#!/usr/bin/env python3
"""TheakosArt static site generator.

Run:  python3 build.py
Writes the Greek site to the repo root and the English site to /en.
All copy, projects and image references live in this one file.

Photos: by default they load from the current theakosart.gr media library.
Run scripts/fetch_images.py once to copy them into assets/img, then rebuild:
any photo found locally is used instead of the remote one.
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.theakosart.gr"
UP = SITE + "/wp-content/uploads/"
PHONE, PHONE_SHOW, EMAIL = "+306949206642", "+30 694 920 6642", "info@theakosart.gr"
MAP = "https://goo.gl/maps/KMDonzc1GKz"
FB = "https://www.facebook.com/pages/TheakosArt-constructions/695661513846411"
IG = "https://instagram.com/theakosart.gr"
LANG = "el"


def L(el, en):
    return el if LANG == "el" else en


def e(s):
    return html.escape(s, quote=True)


def full(thumb):
    """WordPress thumbnail name -> original file name."""
    return re.sub(r"-\d{3,4}x\d{3,4}(\.\w+)$", r"\1", thumb)


def src(path, depth):
    """Use a local copy from assets/img when it exists, else the remote file."""
    name = path.replace("/", "_")
    if os.path.exists(os.path.join(ROOT, "assets", "img", name)):
        return "../" * (depth + (LANG == "en")) + "assets/img/" + name
    return UP + path


def img(path, alt, depth, big=False, lazy=True):
    """big=True asks for the original and falls back to the thumbnail."""
    main = full(path) if big else path
    fb = ""
    if big and main != path:
        fb = ' onerror="this.onerror=null;this.src=\'%s\'"' % src(path, depth)
    return '<img src="%s" alt="%s"%s%s decoding="async">' % (
        src(main, depth), e(alt), ' loading="lazy"' if lazy else "", fb)


# ----------------------------------------------------------------- content
CATS = [
    ("villas", "Βίλες", "Villas"),
    ("hospitality", "Ξενοδοχεία", "Hotels"),
    ("commercial", "Επαγγελματικοί χώροι", "Commercial"),
    ("atelier", "Ατελιέ & 3D", "Atelier & 3D"),
]
REN_EL = ("Ολική ανακαίνιση. Κάθε δωμάτιο σχεδιάστηκε ως ξεχωριστός χώρος, με σεβασμό στο κυκλαδίτικο ύφος "
          "και φινίρισμα αντάξιο της φιλοξενίας που υπόσχεται.")
REN_EN = ("Full renovation. Every room was designed as a space of its own, true to the Cycladic character "
          "and finished to the standard its guests expect.")
MM_EL = ("Δύο βίλες με θέα στο Αιγαίο, για έως 13 επισκέπτες η καθεμία. Πέντε deluxe υπνοδωμάτια με ιδιωτικό λουτρό "
         "και ένα master με δική του εξωτερική πισίνα. Τέχνη και σχεδιασμός, με την ιδιωτικότητα ενός σπιτιού.")
MM_EN = ("Two villas facing the Aegean, each for up to 13 guests. Five deluxe en-suite bedrooms and a master suite "
         "with its own outdoor pool. Art and design, with the privacy of a home.")
# slug, title, place_el, place_en, year, category, image, desc_el, desc_en, scope_el, scope_en
P = [
 ("ftelia-black-villas", "Ftelia Black Villas", "Φτελιά, Μύκονος", "Ftelia, Mykonos", "2025", "villas",
  "2025/11/7f9037431e3d1de082768bd8e459e109-670x458.webp",
  "Νεόδμητο συγκρότημα 500 μέτρα από το Alemagou. 21 σουίτες, η καθεμία με ιδιωτική πισίνα, μαζί με reception, "
  "bar restaurant, χώρους προσωπικού, κουζίνες και parking.",
  "A newly built complex 500 metres from Alemagou. 21 suites, each with a private pool, along with reception, "
  "bar restaurant, staff quarters, kitchens and parking.", "Νέα κατασκευή", "New build"),
 ("mega-mansion-2", "Mega Mansion 2", "Μύκονος", "Mykonos", "2022", "villas",
  "2022/05/mega-mansion2-15-1-670x376.jpg", MM_EL, MM_EN, "Κατασκευή βίλας", "Villa construction"),
 ("mega-mansion-1", "Mega Mansion 1", "Μύκονος", "Mykonos", "2022", "villas",
  "2022/05/mega_mansion1a-3-670x376.jpg", MM_EL, MM_EN, "Κατασκευή βίλας", "Villa construction"),
 ("psarou-black-villa-2", "Psarou Black Villa 2", "Ψαρού, Μύκονος", "Psarou, Mykonos", "2020", "villas",
  "2020/06/002_1025_psaroublack2_20200520-21_pe-670x447.jpg",
  "Η δεύτερη Black Villa στην Ψαρού. Σκούρος όγκος πάνω στον βράχο, ανοιχτός στο φως και στη θάλασσα.",
  "The second Black Villa at Psarou. A dark volume set on the rock, open to the light and the sea.",
  "Κατασκευή βίλας", "Villa construction"),
 ("psarou-black-villa", "Psarou Black Villa", "Ψαρού, Μύκονος", "Psarou, Mykonos", "2019", "villas",
  "2019/05/072_0076_psaroublack_20190429-30-670x361.jpg",
  "Η πρώτη Black Villa στην Ψαρού: μια κατοικία που ξεχωρίζει από το λευκό του νησιού χωρίς να το αρνείται.",
  "The first Black Villa at Psarou: a house that stands apart from the island's white without denying it.",
  "Κατασκευή βίλας", "Villa construction"),
 ("mymykonos-hotel", "MyMykonos Hotel", "Μύκονος", "Mykonos", "2018", "hospitality",
  "2018/06/IMG_2482-670x439.jpg", REN_EL, REN_EN, "Ολική ανακαίνιση", "Full renovation"),
 ("sahas-rooms", "Sahas Rooms", "Μύκονος", "Mykonos", "2018", "hospitality",
  "2018/01/NAN_2435_preview-670x447.jpeg", REN_EL, REN_EN, "Ολική ανακαίνιση", "Full renovation"),
 ("villa-elina", "Villa Elina", "Μύκονος", "Mykonos", "2017", "hospitality",
  "2017/06/IMG_5815-670x445.jpg", REN_EL, REN_EN, "Ολική ανακαίνιση", "Full renovation"),
 ("anastasias-visage", "Anastasia's Visage", "Μύκονος", "Mykonos", "2017", "hospitality",
  "2017/06/IMG_5611-670x443.jpg", REN_EL, REN_EN, "Ολική ανακαίνιση", "Full renovation"),
 ("constantina-zorz-xydakis", "Constantina Zorz Xydakis", "Μύκονος", "Mykonos", "2017", "hospitality",
  "2017/06/IMG_5976-670x670.jpg", REN_EL, REN_EN, "Ολική ανακαίνιση", "Full renovation"),
 ("eternal-suites", "Eternal Suites", "Μύκονος", "Mykonos", "2017", "hospitality",
  "2017/06/IMG_4887-670x502.jpg", REN_EL, REN_EN, "Ολική ανακαίνιση", "Full renovation"),
 ("voula-apartments-rooms", "Voula Apartments & Rooms", "Μύκονος", "Mykonos", "2016", "hospitality",
  "2016/07/210-670x447.jpg", REN_EL, REN_EN, "Ολική ανακαίνιση", "Full renovation"),
 ("ibiscus", "Ibiscus", "Μύκονος", "Mykonos", "2016", "hospitality",
  "2016/07/FullSizeRender-6-670x440.jpg", REN_EL, REN_EN, "Ολική ανακαίνιση", "Full renovation"),
 ("psarou-kaftans-ozar", "Psarou Kaftans & Beachwear, OZAR Jewellery", "Ψαρού, Μύκονος", "Psarou, Mykonos", "2016",
  "commercial", "2016/07/78-670x447.jpg",
  "Κατασκευή δύο καταστημάτων στην Ψαρού.", "Construction of two shops at Psarou.",
  "Κατασκευή καταστημάτων", "Retail construction"),
 ("flaskos-suites", "Flaskos Suites", "Μύκονος", "Mykonos", "2016", "hospitality",
  "2016/07/FullSizeRender-670x442.jpg", REN_EL, REN_EN, "Ολική ανακαίνιση", "Full renovation"),
 ("ibiscus-3d", "Ibiscus Hotel 3D", "Μύκονος", "Mykonos", "2015", "atelier",
  "2015/10/11_SUITE16-24_BAMBOO-670x473.jpg",
  "Σχεδιασμός εσωτερικών και εξωτερικών χώρων, αποτυπωμένος σε φωτορεαλιστικά 3D πριν ξεκινήσει το εργοτάξιο.",
  "Interior and exterior design, shown in photorealistic 3D before work began on site.",
  "Μελέτη & 3D", "Design & 3D"),
 ("yoga-room", "Yoga Room", "Μύκονος", "Mykonos", "2015", "commercial",
  "2015/05/Villa-Konstantin-Mykonos-1-670x456.jpg",
  "Χώρος φτιαγμένος ειδικά για μαθήματα yoga στο νησί.", "A space built for yoga classes on the island.",
  "Ειδική κατασκευή", "Purpose-built space"),
 ("villa-konstantin", "Villa Konstantin", "Μύκονος", "Mykonos", "2015", "hospitality",
  "2015/05/26-670x447.jpg", REN_EL, REN_EN, "Ολική ανακαίνιση", "Full renovation"),
 ("hand-made-furniture", "Hand Made Furniture", "Ατελιέ TheakosArt", "TheakosArt atelier", "2014", "atelier",
  "2014/09/Villa-Konstantin-Mykonos-12_site-670x598.jpg",
  "Χειροποίητα έπιπλα από 100% φυσικό ξύλο, φτιαγμένα για τον χώρο όπου θα ζήσουν.",
  "Handmade furniture in 100% natural wood, made for the room it will live in.",
  "Χειροποίητο έπιπλο", "Handmade furniture"),
 ("homes-athens", "Homes Projects", "Αθήνα", "Athens", "2014", "villas",
  "2014/09/stegazoume-670x502.jpg",
  "Σύγχρονες κατοικίες στην Αθήνα, σχεδιασμένες γύρω από τις ανάγκες των ανθρώπων που τις κατοικούν.",
  "Contemporary homes in Athens, designed around the people who live in them.",
  "Κατοικίες", "Residences"),
 ("oniropetra", "Oniropetra", "Καρπενήσι", "Karpenisi", "2013", "hospitality",
  "2013/12/karpenisi2-670x445.jpg",
  "Έργο φιλοξενίας στο Καρπενήσι: πέτρα, ξύλο και βουνό αντί για ασβέστη και θάλασσα.",
  "A hospitality project in Karpenisi: stone, timber and mountain in place of lime and sea.",
  "Έργο φιλοξενίας", "Hospitality project"),
 ("villa-matina", "Villa Matina", "Μύκονος", "Mykonos", "2013", "hospitality",
  "2013/12/9.jpg", REN_EL, REN_EN, "Ολική ανακαίνιση", "Full renovation"),
 ("vetality", "Vetality Ltd", "Γέρακας, Αττική", "Gerakas, Attica", "2013", "commercial",
  "2013/12/farmakeutiki-580x3621.jpg",
  "Σύγχρονη έδρα για φαρμακευτική εταιρεία ζώων, σε ιδιόκτητο κτίριο της TheakosArt με προηγμένα υλικά κατασκευής.",
  "A modern base for an animal-health company, in a building owned by TheakosArt and fitted with advanced materials.",
  "Επαγγελματικό κτίριο", "Commercial building"),
]
KEYS = ["slug", "title", "pel", "pen", "year", "cat", "img", "del", "den", "sel", "sen"]
PROJECTS = [dict(zip(KEYS, p)) for p in P]

HERO = [  # image, caption el, caption en
 ("2019/05/072_0076_psaroublack_20190429-30.jpg", "Psarou Black Villa, Μύκονος", "Psarou Black Villa, Mykonos"),
 ("2018/06/IMG_2482.jpg", "MyMykonos Hotel, Μύκονος", "MyMykonos Hotel, Mykonos"),
 ("2022/05/mega-mansion2-15-1-670x376.jpg", "Mega Mansion 2, Μύκονος", "Mega Mansion 2, Mykonos"),
 ("2018/06/IMG_2477.jpg", "MyMykonos Hotel, Μύκονος", "MyMykonos Hotel, Mykonos"),
 ("2014/09/theakos_slide.jpg", "Η πινελιά μας στο νησί των ανέμων", "Our mark on the island of the winds"),
 ("2018/06/IMG_2479.jpg", "MyMykonos Hotel, Μύκονος", "MyMykonos Hotel, Mykonos"),
]
WALK = [  # image, title el/en, text el/en  — ordered from outside to inside
 ("2020/06/002_1025_psaroublack2_20200520-21_pe-670x447.jpg", "Απ' έξω", "From outside",
  "Πριν από το κτίριο υπάρχει ο τόπος. Ο βράχος, ο άνεμος, η κλίση του ήλιου αποφασίζουν πρώτοι.",
  "Before the building there is the place. The rock, the wind and the angle of the sun decide first."),
 ("2022/05/mega_mansion1a-3-670x376.jpg", "Στο κατώφλι", "At the threshold",
  "Αυλές, πισίνες και πέργκολες είναι δωμάτια χωρίς οροφή. Τα χτίζουμε με την ίδια ακρίβεια.",
  "Courtyards, pools and pergolas are rooms without a ceiling. We build them with the same precision."),
 ("2018/06/IMG_2477.jpg", "Μέσα", "Inside",
  "Το φως μπαίνει εκεί που το σχεδιάσαμε. Κάθε δωμάτιο έχει τον δικό του χαρακτήρα, κανένα δεν αντιγράφει το διπλανό.",
  "Light enters where we planned it. Each room has a character of its own, and none repeats the one next door."),
 ("2018/01/NAN_2462_preview.jpeg", "Στη λεπτομέρεια", "In the detail",
  "Το έπιπλο φτιάχνεται στο χέρι, για αυτόν τον τοίχο και για αυτόν τον άνθρωπο. Εκεί τελειώνει ένα έργο.",
  "The furniture is made by hand, for this wall and this person. That is where a project is finished."),
]
SERVICES = [
 ("Μελέτη & αδειοδότηση", "Design & permits",
  "Ξεκινάμε από το χαρτί. Αναλαμβάνουμε τις πολεοδομικές άδειες, την αρχιτεκτονική μελέτη και τον σχεδιασμό του εσωτερικού, "
  "και σας δείχνουμε τον χώρο σε φωτορεαλιστικά 3D πριν μπει το πρώτο συνεργείο.",
  "We start on paper. We handle planning permits, architectural design and interiors, and show you the space in "
  "photorealistic 3D before the first crew arrives.",
  ["Πολεοδομικές άδειες", "Αρχιτεκτονικός σχεδιασμός και μελέτες", "Εσωτερική διακόσμηση", "Φωτορεαλιστικά 3D"],
  ["Planning permits", "Architectural design and studies", "Interior design", "Photorealistic 3D"]),
 ("Κατασκευή & ανακαίνιση", "Construction & renovation",
  "Κατοικίες, ξενοδοχεία και επαγγελματικοί χώροι, από τον σκελετό ως το τελικό χρώμα. Ένα συνεργείο, ένας υπεύθυνος, "
  "ένα χρονοδιάγραμμα που τηρείται πριν ανοίξει η σεζόν.",
  "Homes, hotels and commercial spaces, from structure to final coat. One crew, one person accountable, and a "
  "schedule that is met before the season opens.",
  ["Ξηρά δόμηση", "Δάπεδα, μάρμαρα, πέτρα", "Κουφώματα", "Ελαιοχρωματισμοί και τεχνοτροπίες", "Μονώσεις"],
  ["Dry construction", "Floors, marble, stone", "Doors and windows", "Painting and finishes", "Insulation"]),
 ("Εγκαταστάσεις & ενέργεια", "Systems & energy",
  "Ό,τι δεν φαίνεται κρατά το κτίριο ζωντανό. Σχεδιάζουμε και εγκαθιστούμε τα ηλεκτρομηχανολογικά και αναβαθμίζουμε "
  "ενεργειακά το κέλυφος, ώστε ο χώρος να αντέχει στον χρόνο και να κοστίζει λιγότερο.",
  "What you don't see keeps a building alive. We design and install the mechanical and electrical systems and "
  "upgrade the envelope, so the space lasts longer and costs less to run.",
  ["Θέρμανση, κλιματισμός, αερισμός", "Ηλεκτρολογικά", "Ύδρευση, αποχέτευση", "Πυρόσβεση, ανελκυστήρες",
   "Θερμοπρόσοψη, λέβητες"],
  ["Heating, cooling, ventilation", "Electrical", "Plumbing and drainage", "Fire safety, lifts",
   "External insulation, boilers"]),
 ("Ατελιέ ξύλου", "Wood atelier",
  "Τα έπιπλα δεν τα διαλέγουμε από κατάλογο. Τα σχεδιάζουμε και τα φτιάχνουμε στο χέρι από φυσικό ξύλο, "
  "στα μέτρα του χώρου και του ανθρώπου.",
  "We don't pick furniture from a catalogue. We design it and make it by hand in natural wood, to the measure of "
  "the room and the person.",
  ["Χειροποίητα έπιπλα", "Κουζίνες", "Ντουλάπες", "Πόρτες"],
  ["Handmade furniture", "Kitchens", "Wardrobes", "Doors"]),
 ("Εξωτερικοί χώροι", "Outdoor spaces",
  "Κήποι, αυλές και πισίνες που συνεχίζουν το σπίτι προς τη θέα.",
  "Gardens, courtyards and pools that carry the house out towards the view.",
  ["Κήποι", "Πισίνες", "Διαμόρφωση αυλών"], ["Gardens", "Pools", "Courtyards"]),
 ("Ψηφιακή παρουσία", "Digital presence",
  "Για ξενοδοχεία και επιχειρήσεις, παραδίδουμε μαζί με τον χώρο και το website που θα τον δείξει.",
  "For hotels and businesses, we deliver the website that shows the space along with the space itself.",
  ["Website επιχείρησης"], ["Business website"]),
]
STEPS = [
 ("Ακούμε", "We listen", "Τον τόπο, τον προϋπολογισμό, τον τρόπο που θέλετε να ζείτε ή να φιλοξενείτε.",
  "To the site, the budget, and the way you want to live or host."),
 ("Σχεδιάζουμε", "We design", "Αρχιτεκτονική μελέτη και 3D, μέχρι να δείτε ακριβώς αυτό που θα παραλάβετε.",
  "Architectural design and 3D, until you see exactly what you will receive."),
 ("Αδειοδοτούμε", "We license", "Αναλαμβάνουμε τις πολεοδομικές άδειες και κάθε έγκριση.",
  "We take on planning permits and every approval."),
 ("Κατασκευάζουμε", "We build", "Με δικά μας συνεργεία και έναν υπεύθυνο έργου από την αρχή ως το τέλος.",
  "With our own crews and one project lead from start to finish."),
 ("Επιπλώνουμε", "We furnish", "Το ατελιέ μας φτιάχνει τα έπιπλα για τον συγκεκριμένο χώρο.",
  "Our atelier makes the furniture for that specific space."),
 ("Παραδίδουμε", "We hand over", "Έτοιμο χώρο, στην ώρα του, με το κλειδί στο χέρι.",
  "A finished space, on time, ready to live in."),
]
TEAM = [
 ("Πέτρος Θεάκος", "Petros Theakos", "Διευθύνων Σύμβουλος", "Managing Director", "Π", "P"),
 ("Σοφία Θεάκου", "Sofia Theakou", "Διπλωματούχος Αρχιτέκτων", "Architect, Dipl.", "Σ", "S"),
 ("Δημήτριος Θεάκος", "Dimitrios Theakos", "Designer", "Designer", "Δ", "D"),
 ("Παναγιώτης Κουτούπης", "Panagiotis Koutoupis", "Ηλεκτρολόγος Μηχανικός", "Electrical Engineer", "Π", "P"),
]
NAV = [("services.html", "Υπηρεσίες", "Services"), ("works.html", "Έργα", "Works"),
       ("studio.html", "Ομάδα", "Studio"), ("contact.html", "Επικοινωνία", "Contact")]

THETA = ('<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">'
         '<circle cx="50" cy="50" r="46"/><line x1="24" y1="50" x2="76" y2="50"/></svg>')


# ------------------------------------------------------------------ chrome
def page(path, title, desc, body, depth, hero_img=None, current=None):
    r = "../" * depth                       # to this language's root
    assets = r if LANG == "el" else r + "../"
    other = ("en/" + path) if LANG == "el" else path
    other_href = (r + other) if LANG == "el" else (r + "../" + path)
    if path == "404.html":
        other_href = "en/index.html"
    url_el, url_en = SITE + "/" + path, SITE + "/en/" + path
    canon = url_el if LANG == "el" else url_en
    nav = "".join('<a href="%s%s"%s>%s</a>' % (r, h, ' aria-current="page"' if h == current else "", L(a, b))
                  for h, a, b in NAV)
    menu = "".join('<li><a href="%s%s">%s</a></li>' % (r, h, L(a, b))
                   for h, a, b in [("index.html", "Αρχική", "Home")] + NAV)
    ld = {"@context": "https://schema.org", "@type": "GeneralContractor", "name": "TheakosArt", "url": SITE,
          "telephone": PHONE, "email": EMAIL, "sameAs": [FB, IG],
          "address": {"@type": "PostalAddress", "addressLocality": "Mykonos", "addressRegion": "Cyclades",
                      "streetAddress": "Aggelika", "addressCountry": "GR"},
          "areaServed": ["Mykonos", "Cyclades", "Athens", "Greece"]}
    og = UP + full(hero_img or HERO[0][0])
    year = "2026"
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="el" href="{url_el}">
<link rel="alternate" hreflang="en" href="{url_en}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og}">
<meta name="theme-color" content="#0C1A22">
<link rel="icon" href="{assets}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Commissioner:wght@300;400;500&family=GFS+Didot&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{assets}assets/css/main.css">
<script>document.documentElement.classList.add('js');setTimeout(function(){{document.documentElement.classList.add('is-open')}},4500);</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{L("Μετάβαση στο περιεχόμενο", "Skip to content")}</a>
<div class="door" aria-hidden="true"><i></i><i></i><div class="door__mark">{THETA}</div></div>
<header class="hdr">
  <a class="brand" href="{r}index.html" aria-label="TheakosArt">{THETA}<span>TheakosArt</span></a>
  <div class="hdr__right">
    <nav class="nav" aria-label="{L("Κύρια πλοήγηση", "Main")}">{nav}</nav>
    <a href="{other_href}" lang="{L("en", "el")}" hreflang="{L("en", "el")}">{L("EN", "ΕΛ")}</a>
    <button class="burger" aria-expanded="false" aria-controls="menu" data-open="{L("Μενού", "Menu")}" data-close="{L("Κλείσιμο", "Close")}">{L("Μενού", "Menu")}</button>
  </div>
</header>
<div class="menu" id="menu"><ul>{menu}</ul></div>
<main id="main">
{body}
</main>
<footer class="ftr">
  <div class="ftr__top">
    <div><h2>{L("Το επόμενο μοναδικό έργο μπορεί να είναι το δικό σας.", "The next one-of-a-kind project could be yours.")}</h2></div>
    <div><p class="ftr__h">{L("Πλοήγηση", "Navigate")}</p><ul>{"".join('<li><a class="link" href="%s%s">%s</a></li>' % (r, h, L(a, b)) for h, a, b in NAV)}</ul></div>
    <div><p class="ftr__h">{L("Ακολουθήστε", "Follow")}</p><ul>
      <li><a class="link" href="{IG}" target="_blank" rel="noopener">Instagram</a></li>
      <li><a class="link" href="{FB}" target="_blank" rel="noopener">Facebook</a></li></ul></div>
    <div><p class="ftr__h">{L("Επικοινωνία", "Contact")}</p><ul>
      <li><a class="link" href="tel:{PHONE}">{PHONE_SHOW}</a></li>
      <li><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><a class="link" href="{MAP}" target="_blank" rel="noopener">{L("Αγγελικά, Μύκονος", "Aggelika, Mykonos")}</a></li></ul></div>
  </div>
  <p class="ftr__word" aria-hidden="true">TheakosArt</p>
  <div class="ftr__base"><span>© {year} TheakosArt</span><span>37.44° N, 25.35° E</span></div>
</footer>
<script src="{assets}assets/js/main.js" defer></script>
</body>
</html>
"""


def cta():
    return f"""<section class="sec wrap cta">
  <h2 class="d2" data-split>{L("Πείτε μας για τον χώρο σας.", "Tell us about your space.")}</h2>
  <a class="btn" href="{{R}}contact.html">{L("Ξεκινήστε το έργο σας", "Start your project")}</a>
</section>"""


def cat_name(c):
    for k, a, b in CATS:
        if k == c:
            return L(a, b)


def see():
    return L("Δείτε", "View")


# ------------------------------------------------------------------- pages
def home():
    d = 0
    slides = "".join('<div class="hero__slide" data-cap="%s">%s</div>' % (
        e(L(a, b)), img(i, L(a, b), d, big=True, lazy=(n > 0))) for n, (i, a, b) in enumerate(HERO))
    layers = "".join('<div class="walk__layer">%s</div>' % img(w[0], L(w[1], w[2]), d, big=True) for w in WALK)
    wsteps = "".join('<div class="walk__step"><h3 class="d2">%s</h3><p>%s</p></div>' % (L(w[1], w[2]), L(w[3], w[4]))
                     for w in WALK)
    cards = "".join(f"""<a class="card" href="works/{p['slug']}.html" data-cursor="{see()}">
      <div class="media">{img(p['img'], p['title'], d, big=True)}</div>
      <div class="card__meta"><h3>{e(p['title'])}</h3><span class="note">{L(p['pel'], p['pen'])}, {p['year']}</span></div></a>"""
                    for p in PROJECTS[:7])
    svc = "".join(f"""<li class="svc__row"><h3>{L(s[0], s[1])}</h3><p>{L(s[2], s[3])}</p></li>""" for s in SERVICES[:5])
    names = "".join("<span>%s</span>" % e(p["title"]) for p in PROJECTS[:10])
    body = f"""<section class="hero" data-hero>
  {slides}
  <div class="hero__in">
    <h1 class="d1" data-split>{L("Κανένα έργο δεν μοιάζει με άλλο. Ούτε το δικό σας.", "No two projects are alike. Yours won't be either.")}</h1>
    <div class="hero__foot"><span class="hero__cap" aria-live="polite"></span><span class="hero__count">01 / 0{len(HERO)}</span></div>
  </div>
  <div class="hero__bar"></div>
</section>

<section class="sec wrap">
  <div class="grid">
    <h2 class="d3 col-l" data-split>{L("Μελετάμε, κατασκευάζουμε και επιπλώνουμε βίλες, ξενοδοχεία και κατοικίες, στη Μύκονο και σε όλη την Ελλάδα.", "We design, build and furnish villas, hotels and homes, in Mykonos and across Greece.")}</h2>
    <div class="col-r prose" data-fade>
      <p class="lead">{L("Δεν επαναλαμβάνουμε έργα. Κάθε χώρος ξεκινά από λευκό χαρτί: τον τόπο, το φως και τον άνθρωπο που θα τον ζήσει.", "We don't repeat projects. Every space starts from a blank sheet: the place, the light and the person who will live in it.")}</p>
      <p>{L("Γι' αυτό κρατάμε όλη τη δουλειά μέσα στην ομάδα μας, από την πολεοδομική άδεια μέχρι το τελευταίο χειροποίητο έπιπλο. Η ενέργεια που βάζουμε σε ένα έργο φαίνεται στο αποτέλεσμα, και το αποτέλεσμα φέρει το όνομά μας.", "That is why we keep all the work within our own team, from the planning permit to the last handmade piece of furniture. The energy we put into a project shows in the result, and the result carries our name.")}</p>
      <p style="margin-top:32px"><a class="link" href="studio.html">{L("Γνωρίστε την ομάδα", "Meet the studio")}</a></p>
    </div>
  </div>
  <dl class="facts">
    <div><dt data-count="{len(PROJECTS)}">{len(PROJECTS)}</dt><dd>{L("έργα στο δημοσιευμένο αρχείο μας", "projects in our published archive")}</dd></div>
    <div><dt data-count="21">21</dt><dd>{L("σουίτες με ιδιωτική πισίνα στο Ftelia Black Villas", "suites with private pools at Ftelia Black Villas")}</dd></div>
    <div><dt data-count="12">12</dt><dd>{L("ειδικότητες κάτω από μία στέγη", "disciplines under one roof")}</dd></div>
    <div><dt data-count="1">1</dt><dd>{L("υπεύθυνος για όλο το έργο", "team accountable for the whole project")}</dd></div>
  </dl>
</section>

<section class="walk" data-walk aria-label="{L("Περιήγηση από έξω προς τα μέσα", "A walk from outside to inside")}">
  <div class="walk__stage">
    {layers}
    <div class="walk__shade"></div>
    <div class="walk__copy">{wsteps}</div>
    <div class="walk__rail" aria-hidden="true">{"<i><b></b></i>" * len(WALK)}</div>
  </div>
</section>

<section class="rail" data-rail>
  <div class="rail__stage">
    <div class="rail__head"><h2 class="d2" data-split>{L("Επιλεγμένα έργα", "Selected works")}</h2>
      <a class="link" href="works.html">{L("Όλα τα έργα", "All works")}</a></div>
    <div class="rail__track">{cards}</div>
  </div>
</section>

<section class="sec wrap on-ink">
  <div class="grid" style="margin-bottom:clamp(40px,6vw,90px)">
    <h2 class="d2 col-l" data-split>{L("Ένα έργο, μία ομάδα.", "One project, one team.")}</h2>
    <p class="col-r lead" data-fade>{L("Όταν ο αρχιτέκτονας, ο μηχανικός και ο τεχνίτης δουλεύουν μαζί από την πρώτη μέρα, τίποτα δεν χάνεται στη μετάφραση.", "When the architect, the engineer and the craftsman work together from day one, nothing is lost in translation.")}</p>
  </div>
  <ul class="svc">{svc}</ul>
  <p style="margin-top:40px"><a class="btn" href="services.html">{L("Δείτε όλες τις υπηρεσίες", "See all services")}</a></p>
</section>

<div class="marq" aria-hidden="true"><div class="marq__in">{names}{names}</div></div>

<section class="sec wrap">
  <h2 class="d2" data-split style="max-width:11em;margin-bottom:clamp(48px,7vw,100px)">{L("Από το πρώτο σκίτσο ως το κλειδί.", "From first sketch to key.")}</h2>
  <ol class="steps">{"".join('<li data-fade><h3>%s</h3><p>%s</p></li>' % (L(s[0], s[1]), L(s[2], s[3])) for s in STEPS)}</ol>
</section>
<div class="wrap"><div class="rule" data-rule></div></div>
{cta().replace("{R}", "")}"""
    return page("index.html", L("TheakosArt | Κατασκευές και design στη Μύκονο", "TheakosArt | Construction and design in Mykonos"),
                L("Μελέτη, κατασκευή και επίπλωση για βίλες, ξενοδοχεία και κατοικίες στη Μύκονο και σε όλη την Ελλάδα. Κάθε έργο είναι μοναδικό.",
                  "Design, construction and furnishing for villas, hotels and homes in Mykonos and across Greece. Every project is one of a kind."),
                body, d)


def page_hero(image, title, note, d):
    return f"""<section class="hero page-hero">
  <div class="hero__slide is-active">{img(image, title, d, big=True, lazy=False)}</div>
  <div class="hero__in"><h1 class="d1" data-split>{e(title)}</h1>
    <div class="hero__foot"><span>{note}</span></div></div>
</section>"""


def services():
    d = 0
    rows = "".join(f"""<li class="svc__row" data-fade><h3>{L(s[0], s[1])}</h3>
      <div><p>{L(s[2], s[3])}</p><ul>{"".join("<li>%s</li>" % x for x in L(s[4], s[5]))}</ul></div></li>""" for s in SERVICES)
    body = page_hero("2018/06/IMG_2479.jpg", L("Υπηρεσίες", "Services"),
                     L("Από την άδεια ως το έπιπλο", "From permit to furniture"), d) + f"""
<section class="sec wrap">
  <div class="grid">
    <h2 class="d3 col-l" data-split>{L("Όλο το έργο, από έναν συνεργάτη.", "The whole project, from one partner.")}</h2>
    <div class="col-r prose" data-fade><p class="lead">{L("Με πολυετή εμπειρία σε κατασκευές και ανακαινίσεις σπιτιών, ξενοδοχείων και επαγγελματικών χώρων, παραδίδουμε χώρους με σύγχρονη ποιότητα, οικολογική λογική, εξοικονόμηση ενέργειας και αντοχή στον χρόνο.", "With many years in the construction and renovation of homes, hotels and commercial spaces, we deliver spaces with contemporary quality, ecological sense, energy savings and durability.")}</p></div>
  </div>
  <ul class="svc" style="margin-top:clamp(56px,8vw,120px)">{rows}</ul>
</section>
<section class="sec wrap on-ink">
  <h2 class="d2" data-split style="max-width:11em;margin-bottom:clamp(48px,7vw,100px)">{L("Πώς δουλεύουμε", "How we work")}</h2>
  <ol class="steps">{"".join('<li data-fade><h3>%s</h3><p>%s</p></li>' % (L(s[0], s[1]), L(s[2], s[3])) for s in STEPS)}</ol>
</section>
{cta().replace("{R}", "")}"""
    return page("services.html", L("Υπηρεσίες | TheakosArt", "Services | TheakosArt"),
                L("Άδειες, αρχιτεκτονική μελέτη, 3D, κατασκευή, ηλεκτρομηχανολογικά, ενεργειακή αναβάθμιση, χειροποίητα έπιπλα και εξωτερικοί χώροι.",
                  "Permits, architectural design, 3D, construction, mechanical and electrical, energy upgrades, handmade furniture and outdoor spaces."),
                body, d, "2018/06/IMG_2479.jpg", "services.html")


def works():
    d = 0
    fb = '<button data-filter="all" aria-pressed="true">%s</button>' % L("Όλα", "All") + "".join(
        '<button data-filter="%s" aria-pressed="false">%s</button>' % (k, L(a, b)) for k, a, b in CATS)
    tiles = "".join(f"""<a class="tile" href="works/{p['slug']}.html" data-cat="{p['cat']}" data-cursor="{see()}">
      <div class="media" data-aperture>{img(p['img'], p['title'], d)}</div>
      <h3>{e(p['title'])}</h3><p class="note">{L(p['pel'], p['pen'])}, {p['year']}. {cat_name(p['cat'])}</p></a>""" for p in PROJECTS)
    body = f"""<section class="sec wrap" style="padding-top:clamp(140px,18vw,240px)">
  <h1 class="d1" data-split>{L("Έργα", "Works")}</h1>
  <p class="lead" data-fade style="margin-top:28px">{L("%d έργα, κανένα ίδιο με το άλλο. Βίλες, ξενοδοχεία, καταστήματα και έπιπλα, τα περισσότερα στη Μύκονο." % len(PROJECTS), "%d projects, no two the same. Villas, hotels, shops and furniture, most of them in Mykonos." % len(PROJECTS))}</p>
  <div class="filters" role="group" aria-label="{L("Φίλτρο κατηγορίας", "Filter by category")}">{fb}</div>
  <div class="wgrid">{tiles}</div>
</section>
{cta().replace("{R}", "")}"""
    return page("works.html", L("Έργα | TheakosArt", "Works | TheakosArt"),
                L("Βίλες, ξενοδοχεία και επαγγελματικοί χώροι που κατασκεύασε και ανακαίνισε η TheakosArt στη Μύκονο, την Αθήνα και το Καρπενήσι.",
                  "Villas, hotels and commercial spaces built and renovated by TheakosArt in Mykonos, Athens and Karpenisi."),
                body, d, None, "works.html")


def project(i):
    d = 1
    p, nx = PROJECTS[i], PROJECTS[(i + 1) % len(PROJECTS)]
    body = page_hero(p["img"], p["title"], "%s, %s" % (L(p["pel"], p["pen"]), p["year"]), d) + f"""
<section class="sec wrap">
  <div class="grid">
    <h2 class="d3 col-l" data-split>{L(p['sel'], p['sen'])}</h2>
    <div class="col-r prose" data-fade><p class="lead">{L(p['del'], p['den'])}</p></div>
  </div>
  <dl class="spec" data-fade>
    <div><dt>{L("Τοποθεσία", "Location")}</dt><dd>{L(p['pel'], p['pen'])}</dd></div>
    <div><dt>{L("Κατηγορία", "Category")}</dt><dd>{cat_name(p['cat'])}</dd></div>
    <div><dt>{L("Αντικείμενο", "Scope")}</dt><dd>{L(p['sel'], p['sen'])}</dd></div>
    <div><dt>{L("Έτος", "Year")}</dt><dd>{p['year']}</dd></div>
  </dl>
  <figure class="media" data-aperture data-parallax="70" style="aspect-ratio:16/9">{img(p['img'], p['title'], d, big=True)}</figure>
  <p style="margin-top:40px"><a class="link" href="../works.html">{L("Πίσω σε όλα τα έργα", "Back to all works")}</a></p>
</section>
<a class="next" href="{nx['slug']}.html" data-cursor="{see()}">{img(nx['img'], "", d, big=True)}
  <div class="next__in"><span class="note" style="color:#fff">{L("Επόμενο έργο", "Next project")}</span><span class="d2">{e(nx['title'])}</span></div></a>"""
    return page("works/%s.html" % p["slug"], "%s | TheakosArt" % p["title"],
                "%s, %s. %s" % (p["title"], L(p["pel"], p["pen"]), L(p["del"], p["den"])), body, d, p["img"], "works.html")


def studio():
    d = 0
    people = "".join(f"""<li class="person" data-fade><span class="mono" aria-hidden="true">{L(t[4], t[5])}</span>
      <h3>{L(t[0], t[1])}</h3><p class="note">{L(t[2], t[3])}</p></li>""" for t in TEAM)
    body = page_hero("2014/09/theakos_slide.jpg", L("Ομάδα", "Studio"),
                     L("Αρχιτέκτονας, μηχανικός, designer, κατασκευαστής", "Architect, engineer, designer, builder"), d) + f"""
<section class="sec wrap">
  <div class="grid">
    <h2 class="d3 col-l" data-split>{L("Σκεφτόμαστε σαν αρχιτέκτονες. Χτίζουμε σαν τεχνίτες.", "We think like architects. We build like craftsmen.")}</h2>
    <div class="col-r prose" data-fade>
      <p class="lead">{L("Η TheakosArt είναι μια ομάδα όπου η μελέτη και το εργοτάξιο μιλούν την ίδια γλώσσα.", "TheakosArt is a team where the drawing board and the building site speak the same language.")}</p>
      <p>{L("Ο αρχιτέκτονας, ο ηλεκτρολόγος μηχανικός και ο designer κάθονται στο ίδιο τραπέζι με αυτόν που θα υπογράψει την παράδοση. Έτσι κάθε απόφαση παίρνεται μία φορά και σωστά, και εσείς έχετε έναν άνθρωπο να μιλήσετε για όλα.", "The architect, the electrical engineer and the designer sit at the same table as the person who signs the handover. Each decision is made once and made well, and you have one person to talk to about everything.")}</p>
      <p>{L("Δουλεύουμε κυρίως στη Μύκονο, όπου ο χρόνος είναι λίγος και οι απαιτήσεις υψηλές. Εκεί μάθαμε να υποσχόμαστε μόνο ό,τι παραδίδουμε.", "We work mostly in Mykonos, where time is short and standards are high. That is where we learned to promise only what we deliver.")}</p>
    </div>
  </div>
</section>
<section class="sec wrap on-ink">
  <h2 class="d2" data-split style="margin-bottom:clamp(48px,7vw,100px)">{L("Οι άνθρωποι", "The people")}</h2>
  <ul class="people">{people}</ul>
</section>
<section class="sec wrap">
  <div class="grid">
    <figure class="media col-l" data-aperture data-parallax="50" style="aspect-ratio:4/5">{img("2018/01/NAN_2462_preview.jpeg", L("Χειροποίητο έπιπλο TheakosArt", "Handmade furniture by TheakosArt"), d, big=True)}</figure>
    <div class="col-r" style="align-self:center">
      <h2 class="d3" data-split>{L("Τρεις αρχές που δεν διαπραγματευόμαστε.", "Three principles we don't negotiate.")}</h2>
      <ul class="svc" style="margin-top:36px">
        <li class="svc__row" style="grid-template-columns:1fr"><p>{L("Κάθε έργο σχεδιάζεται από την αρχή. Δεν υπάρχει έτοιμη λύση για έναν μοναδικό χώρο.", "Every project is designed from scratch. There is no ready-made answer for a one-of-a-kind space.")}</p></li>
        <li class="svc__row" style="grid-template-columns:1fr"><p>{L("Σεβόμαστε τον τόπο. Στις Κυκλάδες, το κτίριο οφείλει να ανήκει στο τοπίο.", "We respect the place. In the Cyclades, a building has to belong to the landscape.")}</p></li>
        <li class="svc__row" style="grid-template-columns:1fr"><p>{L("Χτίζουμε για να αντέξει: ποιοτικά υλικά, ενεργειακή λογική, λεπτομέρεια που δεν φθείρεται.", "We build to last: quality materials, energy sense, detail that does not wear.")}</p></li>
      </ul>
    </div>
  </div>
</section>
{cta().replace("{R}", "")}"""
    return page("studio.html", L("Ομάδα | TheakosArt", "Studio | TheakosArt"),
                L("Η ομάδα της TheakosArt: αρχιτέκτονας, ηλεκτρολόγος μηχανικός, designer και διεύθυνση έργου σε ένα τραπέζι.",
                  "The TheakosArt team: architect, electrical engineer, designer and project direction at one table."),
                body, d, "2014/09/theakos_slide.jpg", "studio.html")


def contact():
    d = 0
    f = {"n": L("Όνομα", "Name"), "e": "Email", "t": L("Τηλέφωνο", "Phone"), "k": L("Είδος έργου", "Type of project"),
         "w": L("Τοποθεσία έργου", "Project location"), "m": L("Πείτε μας για το έργο", "Tell us about the project")}
    opts = "".join("<option>%s</option>" % x for x in L(
        ["Βίλα ή κατοικία", "Ξενοδοχείο", "Επαγγελματικός χώρος", "Ανακαίνιση", "Χειροποίητα έπιπλα", "Άλλο"],
        ["Villa or home", "Hotel", "Commercial space", "Renovation", "Handmade furniture", "Other"]))
    body = f"""<section class="sec wrap" style="padding-top:clamp(140px,18vw,240px)">
  <h1 class="d1" data-split>{L("Ας μιλήσουμε για το έργο σας.", "Let's talk about your project.")}</h1>
  <div class="grid" style="margin-top:clamp(56px,8vw,120px)">
    <div class="col-l big-contact" data-fade>
      <a class="link" href="tel:{PHONE}">{PHONE_SHOW}</a>
      <a class="link" href="mailto:{EMAIL}">{EMAIL}</a>
      <p style="margin-top:36px">{L("Αγγελικά, Μύκονος 846 00", "Aggelika, Mykonos 846 00, Greece")}</p>
      <p><a class="link" href="{MAP}" target="_blank" rel="noopener">{L("Άνοιγμα στον χάρτη", "Open in Maps")}</a></p>
      <p class="note" style="margin-top:36px;max-width:26em">{L("Αναλαμβάνουμε έργα στη Μύκονο, τις Κυκλάδες, την Αττική και την υπόλοιπη Ελλάδα.", "We take on projects in Mykonos, the Cyclades, Attica and the rest of Greece.")}</p>
    </div>
    <form class="col-r form" data-mailform data-to="{EMAIL}" data-subject="{L("Νέο έργο", "New project")}" data-namefield="{f['n']}" data-fade>
      <label>{f['n']}<input name="{f['n']}" autocomplete="name" required></label>
      <label>{f['e']}<input name="{f['e']}" type="email" autocomplete="email" required></label>
      <label>{f['t']}<input name="{f['t']}" type="tel" autocomplete="tel"></label>
      <label>{f['k']}<select name="{f['k']}">{opts}</select></label>
      <label class="full">{f['w']}<input name="{f['w']}"></label>
      <label class="full">{f['m']}<textarea name="{f['m']}" required></textarea></label>
      <div class="full"><button class="btn" type="submit">{L("Στείλτε το μήνυμα", "Send message")}</button>
        <p class="note" data-formstatus hidden style="margin-top:14px">{L("Το μήνυμα άνοιξε στην εφαρμογή email σας. Πατήστε αποστολή εκεί για να το λάβουμε.", "Your message opened in your email app. Press send there so it reaches us.")}</p></div>
    </form>
  </div>
</section>
<figure class="media" data-parallax="80" style="height:70vh">{img("2018/06/IMG_2482.jpg", "MyMykonos Hotel", d, big=True)}</figure>"""
    return page("contact.html", L("Επικοινωνία | TheakosArt", "Contact | TheakosArt"),
                L("Επικοινωνήστε με την TheakosArt στη Μύκονο: %s, %s." % (PHONE_SHOW, EMAIL),
                  "Contact TheakosArt in Mykonos: %s, %s." % (PHONE_SHOW, EMAIL)), body, d, None, "contact.html")


def notfound():
    body = f"""<section class="sec wrap" style="padding-top:clamp(160px,20vw,260px);min-height:80vh">
  <h1 class="d1">{L("Αυτή η πόρτα δεν οδηγεί πουθενά.", "This door leads nowhere.")}</h1>
  <p class="lead" style="margin:28px 0 40px">{L("Η σελίδα που ζητήσατε δεν υπάρχει ή μετακινήθηκε.", "The page you asked for does not exist or has moved.")}</p>
  <a class="btn" href="/">{L("Επιστροφή στην αρχική", "Back to home")}</a></section>"""
    return page("404.html", "404 | TheakosArt", "404", body, 0)


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def main():
    global LANG
    urls = []
    for LANG in ("el", "en"):
        pre = "" if LANG == "el" else "en/"
        pages = {"index.html": home(), "services.html": services(), "works.html": works(),
                 "studio.html": studio(), "contact.html": contact()}
        for i, p in enumerate(PROJECTS):
            pages["works/%s.html" % p["slug"]] = project(i)
        for rel, text in pages.items():
            write(pre + rel, text)
            urls.append(SITE + "/" + pre + rel)
    LANG = "el"
    write("404.html", notfound())
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join("  <url><loc>%s</loc></url>\n" % u for u in urls) + "</urlset>\n")
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE)
    write(".nojekyll", "")
    imgs = sorted({x for p in PROJECTS for x in (p["img"], full(p["img"]))} | {full(h[0]) for h in HERO} | {h[0] for h in HERO}
                  | {full(w[0]) for w in WALK} | {w[0] for w in WALK})
    write("scripts/images.txt", "\n".join(imgs) + "\n")
    print("built %d pages, %d image references" % (len(urls) + 1, len(imgs)))


if __name__ == "__main__":
    main()
