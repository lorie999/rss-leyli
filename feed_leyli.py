import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

# ---- CONFIGURACIÓ ----
URL = "https://alternativestheatrales.be/auteur/leyli/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ---- DESCARREGUEM LA PÀGINA ----
print("Descarregant la pàgina...")
resposta = requests.get(URL, headers=HEADERS)

if resposta.status_code != 200:
    print(f"❌ Error: la web ha respost amb codi {resposta.status_code}")
    exit()

print("✅ Pàgina descarregada correctament")
sopa = BeautifulSoup(resposta.text, "html.parser")

# ---- CREEM EL FEED ----
fg = FeedGenerator()
fg.title("Leyli Daryoush - Alternatives Théâtrales")
fg.link(href=URL)
fg.description("Articles de Leyli Daryoush a Alternatives Théâtrales")

# ---- BUSQUEM ELS ARTICLES ----
articles = sopa.find_all("h3")

if not articles:
    print("⚠️ No s'han trobat articles.")
else:
    print(f"Trobats {len(articles)} articles")

for h3 in articles:
    link_tag = h3.find("a", href=True)
    if not link_tag:
        continue

    titol = link_tag.get_text(strip=True)
    link = link_tag["href"]

    # Busquem la imatge al contenidor pare
    contenidor = h3.find_parent()
    imatge_tag = contenidor.find("img") if contenidor else None
    imatge_url = ""
    if imatge_tag:
        imatge_url = imatge_tag.get("src", "") or imatge_tag.get("data-src", "")

    if imatge_url:
        descripcio = f'<img src="{imatge_url}" /><br/>{titol}'
    else:
        descripcio = titol

    fe = fg.add_entry()
    fe.title(titol)
    fe.link(href=link)
    fe.content(descripcio, type="html")
    print(f"  → {titol[:60]}...")

# ---- GUARDEM EL FITXER ----
fg.rss_file("leyli.rss")
print("\n✅ Feed guardat com a leyli.rss")