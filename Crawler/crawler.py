import crawl_classes
import ssl


# SSL Zertifikatsfehler ignorieren
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Initiale Daten aus einer Text-Flatfile extrahieren
flatfiler = crawl_classes.Flatfiler()
initial_links = flatfiler.get_initial_links()

# Instanzierung des Crawler-Objektes
crawler = crawl_classes.Crawler(test_run = True)

# Erstellen einer Results-Liste und Erstellen einer Iterator-Variable
crawl_results = []
i = 0

# Durchlauf eines Scrape-Runs für alle initialen Links und Hinzufügen zur
# Ergebnisliste. Hier Anpassung an das Handling innerhalb von Django notwendig!
for link in initial_links:

    crawl_results.append(crawler.scrape(link))
    i += 1

# Print der Ergebnisse und testweise Erstellung einer txt-Datei
# Hier Integration in die Django-DB notwenig
# -> Ausgabeformat in crawl_results: [{'comments':[], 'track_json':{}}, {...}]
print(crawl_results)
with open('result_file.txt', 'w') as f:
    for item in crawl_results:
        f.write("%s\n" % item)
