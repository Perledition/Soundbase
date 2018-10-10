from django.db import models

""" Hier kannst du weitere Felder hinzufügen, die in die Datenbank übernommen werden sollen.. Die Daten können auch erstmal recht grob eingelesenen werden. Sobald der Crawler läuft
    und wir mehr Daten in die Datenbank führen können, kümmere ich mich um das Data Cleansing und die Auswertung.

    1. Für Zusätzliche Felder Achte auf die Typisierung (CharField, IntegerField, BooleanField, EmailField etc. )
    2. Wenn du eine weitere Datenbank anlegen möchtest, kannst du dich an dem ElectronicData Model orientieren
    3. Nicht vergessen, das Model auch in views.py und admin.py zu importieren, wenn ein Zugriff darauf erfolgen sollen
    4. Anschließend auch python manage.py makemigrations und migrate nicht vergesse :) """


class ElectronicData(models.Model):
    Artist = models.CharField(max_length=100)
    song_title = models.CharField(max_length=50)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.song_title
