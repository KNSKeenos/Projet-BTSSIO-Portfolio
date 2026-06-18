import feedparser
from datetime import datetime
import json

def extraire_image(article, nom_site):
    """Tente de trouver une image dans l'article, sinon renvoie une image par défaut."""
    # balises média de feedparser
    if 'media_content' in article and len(article.media_content) > 0:
        return article.media_content[0].get('url')
        
    #fichiers joints (enclosures)
    if 'enclosures' in article and len(article.enclosures) > 0:
        for enc in article.enclosures:
            if enc.get('type', '').startswith('image/'):
                return enc.get('url')
                
    # Image de secours si image du site non trouvé
    images_secours = {
        "CERT-FR": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=400", 
        "Sécurité Debian": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=400", 
        "IT-Connect": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400", 
    }
    # Renvoie image secours si image site non trouvé
    return images_secours.get(nom_site, "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400")
    #flux rss des sites (peut être ajouté, ne pas oublié , : et ""
def generer_json_veille():
    sources_rss = {
        "IT-Connect": "https://www.it-connect.fr/feed/",
        "Journal du Hacker": "https://www.journalduhacker.net/rss",
        "Korben": "https://korben.info/feed/",
        "CERT-FR": "https://www.cert.ssi.gouv.fr/alerte/feed/",
        "ZDNET": "https://www.zdnet.fr/feeds/rss/actualites/",
        "Sécurité Debian": "https://www.debian.org/security/dsa-long.fr.rdf", 
        "Blog Officiel Zabbix": "https://blog.zabbix.com/feed/",
        "Actualités Dolibarr": "https://www.dolibarr.fr/forum/latest.rss"
    }
    
    donnees_site_web = {}

    for nom_site, url_flux in sources_rss.items():
        flux = feedparser.parse(url_flux)
        if not flux.entries:
            continue

        donnees_site_web[nom_site] = []

        for article in flux.entries[:10]:
            date_brute = article.get('published_parsed') or article.get('updated_parsed')
            date_pub = datetime(*date_brute[:6]).strftime("%d/%m/%Y") if date_brute else "Date inconnue"
            
            # Extraction de l'image de l'article si trouvé
            image_url = extraire_image(article, nom_site)
                
            donnees_site_web[nom_site].append({
                "titre": article.title,
                "lien": article.link,
                "date": date_pub,
                "image": image_url # <-- Ajout de l'image dans le JSON
            })

    with open("veille.json", "w", encoding="utf-8") as fichier_json:
        json.dump(donnees_site_web, fichier_json, ensure_ascii=False, indent=4)
        
    print("[*] Fichier veille.json généré avec les illustrations !")

if __name__ == "__main__":
    generer_json_veille()
