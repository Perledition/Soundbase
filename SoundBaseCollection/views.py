from django.shortcuts import render
from django.views.generic import View
from .models import ElectronicData
from .crawl_classes import Validator, MainClass, Flatfiler, Crawler
import ssl
import json


# In diesem View kann der Crawler integriert werden.
class IndexView(View):
    template_name = 'SoundBaseCollection/Index.html'

    # Das ist die Baustelle für den Crawler
    def post(self, request):
        # Post Daten einlesen und keywords in Liste convertieren
        search_token = request.POST['search'].lower().split(',')

        # SSL Zertifikatsfehler ignorieren
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        flatfiler = Flatfiler()
        initial_links = flatfiler.get_initial_links(search_token)
        print(initial_links)

        # Instanzierung des Crawler-Objektes
        crawler = Crawler(test_run = True)

        # Erstellen einer Results-Liste und pflegt die Tracks in die Data (Zwischendatenbank ein)
        crawl_results = crawler.scrape(initial_links)
        for J_track in crawl_results:
            #J_track = json.dumps(track)
            song = ElectronicData()
            # song.Artist = J_track['track_json']['publisher_metadata']['artist']
            song.song_title = J_track['track_json']['title']
            song.link = J_track['track_json']['permalink_url']
            song.comment_count = J_track['track_json']['comment_count']
            song.likes_count = J_track['track_json']['likes_count']
            # song.created_at = J_track['track_json']['created_at']
            # song.last_modified = J_track['track_json']['last_modified']
            # song.release_date = J_track['track_json']['release_date']
            song.download_count = J_track['track_json']['download_count']
            song.duration = J_track['track_json']['duration']
            song.full_duration = J_track['track_json']['full_duration']
            song.playback_count = J_track['track_json']['playback_count']
            song.reposts_count = J_track['track_json']['reposts_count']
            song.tag_list = J_track['track_json']['tag_list']
            song.uri = 'https://w.soundcloud.com/player/?url=https%3A//{}&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true'.format(J_track['track_json']['uri'][8:])

            song.save()

        return render(request, self.template_name, {'sum': len(crawl_results)})

    # Diese Funktion ruft einfach nur den Zustand und muss deshalb auch nicht mehr angepasst werden.
    def get(self, request):
        return render(request, self.template_name, {'sum':0})

# Der View kann erstmal unverändert bleiben, der der Fokus auf der Crawler integration und dem ML-Algorythmus liegt.
class ElectroView(View):
    # Standardisiertes Template und der datapoint stellt die Datenbank verbindung her.
    template_name = 'SoundBaseCollection/BoxTemplate.html'
    datapoint = ElectronicData.objects.all()

    # Arbeitsschritt für später
    def post(self, request, song_id):
        """ An dieser Stelle wird der Postman integriert. Wenn sich für eine Verföffentlichung entschieden wurde muss der Request ausgeführt werden. Ob mit API oder ohne.
            Bevor das Script allerdings in den View eingebettet wird, sollte es über ein normales Rohscript funktionieren, damit wir hier nicht alles zumüllen. """

        track = ElectronicData.objects.get(id=song_id)
        track.used = 1
        track.save()

        return render(request, self.template_name, {'datapoint':self.datapoint, 'Genere':'Electronic'})

    # Diese Funktion ruft einfach nur den Zustand und muss deshalb auch nicht mehr angepasst werden.
    def get(self, request):
        return render(request, self.template_name, {'datapoint':self.datapoint, 'Genere':'Electronic'})

# Diese Views sind ersteinmal nur Dummys. Wenn der Crawler und Algorythmus richtig für den Electronic Sound implementiert sind, kann auf andere Generes ausgeweitet werden.
class RockView(View):
    template_name = 'SoundBaseCollection/BoxTemplate.html'
    datapoint = ElectronicData.objects.all()

    def post(self, request):
        pass

    def get(self, request):
        return render(request, self.template_name, {'datapoint':self.datapoint, 'Genere':'Rock'})

class JazzView(View):
    template_name = 'SoundBaseCollection/BoxTemplate.html'
    datapoint = ElectronicData.objects.all()

    def post(self, request):
        pass

    def get(self, request):
        return render(request, self.template_name, {'datapoint':self.datapoint, 'Genere':'Jazz'})
