from django.shortcuts import render
from django.views.generic import View
from .models import ElectronicData


# In diesem View kann der Crawler integriert werden.
class IndexView(View):
    template_name = 'SoundBaseCollection/Index.html'

    # Das ist die Baustelle für den Crawler
    def post(self, request):

        """ Der Crawler sollte in diese Post Funktion eingegliedert werden. Die Funktionen, die du erstellt hast, können erhalten bleiben
            Am Ende muss nur die Post Funktion die ausführende sein. Das sollte eigentlich kein Problem darstellen
            Interessant ist, wie die Performance das ausgleicht.. Mit wenn das Grundsätzlich läuft können wir auch die Ergebnisse tracken, das wird aber ein bisschen Fummelarbeit mit Java Script."""

        search_token = request.POST['search']
        pass

    # Diese Funktion ruft einfach nur den Zustand und muss deshalb auch nicht mehr angepasst werden.
    def get(self, request):
        return render(request, self.template_name)

# Der View kann erstmal unverändert bleiben, der der Fokus auf der Crawler integration und dem ML-Algorythmus liegt.
class ElectroView(View):
    # Standardisiertes Template und der datapoint stellt die Datenbank verbindung her.
    template_name = 'SoundBaseCollection/BoxTemplate.html'
    datapoint = ElectronicData.objects.all()

    # Arbeitsschritt für später
    def post(self, request):
        """ An dieser Stelle wird der Postman integriert. Wenn sich für eine Verföffentlichung entschieden wurde muss der Request ausgeführt werden. Ob mit API oder ohne.
            Bevor das Script allerdings in den View eingebettet wird, sollte es über ein normales Rohscript funktionieren, damit wir hier nicht alles zumüllen. """
        pass

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
