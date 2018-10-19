import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup as bs
import requests
import sqlite3
import json
import lxml
import sys
import random


class Validator(object):

    # Allgemeine Validator-Klassenvariablen
    max_track_duration = 600000
    max_track_play_count = 8000
    latest_upload_date = None

    # METHODEN

    # Methode überprüft, ob der Wert hint dem JSON key 'kind' den String
    # 'track' enthält, bzw. ob eine Liste mit der ID '68' existiert
    def is_track(self, link_json):

        condition_source_1 = 'kind'
        condition_string = 'track'

        if link_json is not None and link_json[condition_source_1] == \
        condition_string:
            return True
        else:
            return False
        return False


    # Methode überprüft, ob der Wert hinter dem JSON key 'full_duration'
    # größer als der Wert der Klassenvariable max_track_duration ist
    def is_mix(self, track_json):

        condition_source_1 = 'full_duration'

        if track_json[condition_source_1] >= self.max_track_duration:
            return True
        else:
            return False


    # AUSBAUEN! Vielleicht hier schon "Purchase_URL" nach entsprechenden
    # Download-Gate Anbietern vorfiltern
    # ------------------------------------------------------------------
    # Methode überprüft, ob der JSON key 'purchase_title' den String 'free' in
    # irgendeiner Weise enthält und überprüft dann, ob der Wert hinter dem
    # JSON key 'purchase_url' einen Wert enthält
    def is_free_download(self, track_json):

        condition_source_1 = 'purchase_title'
        condition_source_2 = 'purchase_url'
        condition_string = 'free'

        free_download_or_not = track_json[condition_source_1]
        if free_download_or_not is not None:
            if condition_string in free_download_or_not.lower().strip() and \
            track_json[condition_source_2] is not None:
                    return True

        # Auskommentiert, da Soundcloud teilweise inkonsistente Daten liefert

        # free_download_or_not = track_json['downloadable']
        # if free_download_or_not is not None:
        #     if free_download_or_not == True and track_json['download_url'] \
        #     is not None:
        #             return True
        #
        # return False


    # Methode soll prüfen, ob der Wert hinter dem JSON key 'display_date' vor
    # einem festgelegten Stichtag liegt
    def is_up_to_date(self):

        condition_source_1 = 'display_date'
        # Verwende Klassenvariable = self.latest_upload_date
        pass


    # Methode überprüft, ob der Wert hinter dem JSON key 'playback_count'
    # größer als der Wert der Variable max_track_play_count ist
    def enough_plays(self, track_json):

        condition_source_1 = 'playback_count'

        if track_json[condition_source_1] >= self.max_track_play_count:
            return True
        else:
            return False


class MainClass(object):

    # Allgemeine Oberklassenvariablen
    base_url = 'https://soundcloud.com'
    search_url = str(base_url) + '/search/sounds?q={}'
    val = Validator()


    # OBERKLASSENMETHODEN

    # Methode liefert eine von BeautifulSoup geparstes Object zurück
    def soup_it(self, link_to_soup):

        html = requests.get(link_to_soup)
        soup = bs(html.text, 'lxml')
        return soup


    # Methode extrahiert die relevanten JSON-Teile aus dem Soup-Objekt
    def extract_json(self, soup_to_extract):

        for tag in soup_to_extract.select('script'):
            if str(tag.text).startswith('webpackJsonp'):
                json_as_str = tag.text[279:-163]
                try:
                    json_load = json.loads(json_as_str)
                except json.decoder.JSONDecodeError:
                    return None

                for json_dict in json_load:
                    if json_dict['id'] == 68:
                        json_extract = json_dict['data'][0]
                        return json_extract


class Flatfiler(MainClass):

    # Initialisierung
    def __init__(self):

        self.flatfile_name = 'flatfile'
        self.search_terms = self.get_search_items()
        self.initial_links = []

    # METHODEN

    # Methode wird bei Objektinstanzierung aufgerufen und extrahiert sämtlichen
    # Wörter aus der übergebenen Textdatei
    def get_search_items(self):

        try:
            search_terms = [term.strip().lower() for term in \
            open(self.flatfile_name)]
            return search_terms

        except FileNotFoundError as err:
            print('Flatfile could not be found: ' + str(err))
            return None


    # Methode setzt jeden Wert der internen Liste search_terms in die
    # Soundcloud Suchmaske ein und extrahiert die URLs für Tracks (Profile und)
    # Mixe werden hier bereits vorgefiltert
    def get_initial_links(self):

        try:

            for term in self.search_terms:
                soup = self.soup_it(self.search_url.format(\
                str(term.replace(' ', '%20'))))
                temp = [search_item.get('href') for search_item in \
                soup.select('noscript ul li h2 a')]
                for initial_link in temp:
                    initial_soup = self.soup_it(str(self.base_url) + \
                    str(initial_link))
                    initial_json = self.extract_json(initial_soup)

                    if self.val.is_track(initial_json) and not \
                    self.val.is_mix(initial_json):
                        self.initial_links.append(initial_link)

            return self.initial_links

        except AttributeError as err:
            print('Cannot soup initital links because of ' + str(err))
            return None


class Crawler(MainClass):

    # Initialisierung
    def __init__(self, scraping_amount = 'small', test_run = False):

        # Festlegen der zu crawlenden Links pro Run (Standard = "small")
        # Optional: test_run = True -> max. 10 Links pro Run
        if test_run == True:
            self.max_pages_per_initial_link = 10
            print(str(test_run) + ' = ' + str(self.max_pages_per_initial_link))
        elif scraping_amount == 'medium':
            self.max_pages_per_initial_link = 100
        elif scraping_amount == 'large':
            self.max_pages_per_initial_link = 250
        elif scraping_amount == 'small':
            self.max_pages_per_initial_link = 50

        # Initialisieren der Results-Liste für den Return
        self.results = []
        # Initialisieren des false_count (max_pages_per_initial_link + 1,
        # da so nicht vor Erreichen der gewollten Iterationen abgebrochen wird)
        # Der false_count dient dazu Endlosschleifen aufgrund der Recommend-
        # Engine zu vermeiden. Nach x-Iterationen muss abgebrochen werden.
        self.false_count = self.max_pages_per_initial_link + 1

    # METHODEN

    # Methode wird ein Keyword übergeben, welches dann in die Soundcloud
    # Suchmaske eingefügt wird, um so initale Links für einen Crawler-Run
    # zu generieren
    def get_initial_links(self, keyword):

            try:
                initial_links = []

                soup = self.soup_it(self.search_url.format(\
                str(keyword.replace(' ', '%20'))))
                temp = [search_item.get('href') for search_item in \
                soup.select('noscript ul li h2 a')]

                for initial_link in temp:
                    initial_soup = self.soup_it(str(self.base_url) + \
                    str(initial_link))
                    initial_json = self.extract_json(initial_soup)

                    if self.val.is_track(initial_json) and not \
                    self.val.is_mix(initial_json):
                        self.initial_links.append(initial_link)

                return self.initial_links

            except AttributeError as err:
                print('Cannot soup initital links because of ' + str(err))
                return None


    def get_next_suggested_tracks(self, link_to_soup):

        suggested_html = requests.get(link_to_soup + '/recommended')

        suggested_soup = bs(suggested_html.text, 'lxml')

        suggested_links = [suggested_link.get('href') for suggested_link in \
        suggested_soup.select('section a')]


        suggested_tracks = []
        for suggested_link in suggested_links:
            suggested_soup = self.soup_it(str(self.base_url) + \
            str(suggested_link))
            suggested_json = self.extract_json(suggested_soup)
            if self.val.is_track(suggested_json):
                suggested_tracks.append(suggested_link)

        return suggested_tracks


    def get_comments(self,link_soup):

        comments = [comment.text.strip() for comment in \
        link_soup.select('."comments" p')]

        return comments


    def scrape(self, link_to_scrape):

        # n ist die Iterationsvariable für den Scraper und dient dem Abgleich
        # mit max_pages_per_initial_link
        n = 0

        print(n)

        # Zusammensetzen des initialen Links
        link_to_soup = str(self.base_url) + str(link_to_scrape)

        while n <= self.max_pages_per_initial_link:

            link_soup = self.soup_it(link_to_soup)

            link_json = self.extract_json(link_soup)

            print('mix: ', self.val.is_mix(link_json))
            print('free download: ', self.val.is_free_download(link_json))

            if not self.val.is_mix(link_json) and \
            self.val.is_free_download(link_json):

                comments_temp = self.get_comments(link_soup)
                track_info = {}
                track_info['comments'] = comments_temp
                track_info['track_json'] = link_json
                # Überprüfen, ob die Trackdaten schon existieren
                # muss am besten in der Datenbank nochmal über Pandas
                # nachträglich gecheckt werden
                if track_info not in self.results:

                    self.results.append(track_info)
                    n += 1
                    print(n)
            else:
                self.false_count += 1
                if self.false_count >= 5:
                    break

            # Sammeln aller vorgeschlagenen Links für den nächsten
            # potentenziellen Track
            suggested_tracks = self.get_next_suggested_tracks(link_to_soup)

            # Den neuen Link für die nächsten while-Iteration zusammensetzen
            # und der link_to_soup Variable zuweisen
            new_link = str(self.base_url) + suggested_tracks[ \
            random.randrange(len(suggested_tracks))]
            link_to_soup = new_link

        return self.results

# Platzhalterklasse für das Parsen der Scrape-Ergebnisse und Übertrag in die DB
class DBHandler(object):

    pass
