from django.db import models
from datetime import*

""" Hier kannst du weitere Felder hinzufügen, die in die Datenbank übernommen werden sollen.. Die Daten können auch erstmal recht grob eingelesenen werden. Sobald der Crawler läuft
    und wir mehr Daten in die Datenbank führen können, kümmere ich mich um das Data Cleansing und die Auswertung.

    1. Für Zusätzliche Felder Achte auf die Typisierung (CharField, IntegerField, BooleanField, EmailField etc. )
    2. Wenn du eine weitere Datenbank anlegen möchtest, kannst du dich an dem ElectronicData Model orientieren
    3. Nicht vergessen, das Model auch in views.py und admin.py zu importieren, wenn ein Zugriff darauf erfolgen sollen
    4. Anschließend auch python manage.py makemigrations und migrate nicht vergesse :) """

### Data ist eine Zwischenlagerung der Crawler Elemente ###

class ElectronicData(models.Model):
    Artist = models.CharField(max_length=100, default='Unknown')
    song_title = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    comment_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    last_modified = models.DateTimeField(default=datetime.now)
    release_date = models.DateTimeField(default=datetime.now)
    download_count = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    full_duration = models.IntegerField(default=0)
    playback_count = models.IntegerField(default=0)
    reposts_count = models.IntegerField(default=0)
    tag_list = models.CharField(max_length=3000, default='Electronic, Deep House')
    uri = models.CharField(max_length=400, default='Not included')
    used = models.IntegerField(default=0)

    def __str__(self):
        return self.song_title


### Base ist die tatsächlich genutzte Datenbank

class ElectronicBase(models.Model):
    Artist = models.CharField(max_length=100, default='Unknown')
    song_title = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    comment_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    last_modified = models.DateTimeField(default=datetime.now)
    release_date = models.DateTimeField(default=datetime.now)
    download_count = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    full_duration = models.IntegerField(default=0)
    playback_count = models.IntegerField(default=0)
    reposts_count = models.IntegerField(default=0)
    tag_list = models.CharField(max_length=3000, default='Electronic, Deep House')
    uri = models.CharField(max_length=400, default='Not included')
    used = models.IntegerField(default=0)

    def __str__(self):
        return self.song_title
