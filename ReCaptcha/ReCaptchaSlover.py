
# Software zum Lösen von Googles ReCaptchas

# Imports und Dependencies
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import speech_recognition as sr
from pydub import AudioSegment



class ReCaptchaMaintain():
    """
    :param url: ist die URL auf der das ReCaptcha gelöst wird. Kann später als
                Test = True deklaiert werden
    :param timeout: Sekundenabgabe, wie lange auf Events und Ladezeiten gewartet
                werden soll. Angabe erfolgt als int

    Diese Klasse dient der Wartung des ReCaptchaSlover, damit Variablen einfach
    gepflegt werden können und auch für User zugänglich sind, die die Klasse nicht
    in ihrer Gesamtheit verstehen müssen
    """

    # Test Variablen
    url = "https://patrickhlauke.github.io/recaptcha/"
    timeout = 10

# Captcha Lösung
class ReCaptchaSlover(ReCaptchaMaintain):
    """
    Alle Variablen wie das Timeout oder die URL werden über ReCaptchaMaintain
    definiert und geerbt.

    Diese Funktion löst ein Google ReCaptcha automatisch
    """

    def __init__(self):
        pass

    def get_CaptchaAudio(self):
        """
        Diese Funktion öffnet derzeit einen Link und Click sich durch das
        dort vorhandene ReCaptcha bis zur Audio Datei. Wenn die Funktion später
        integriert werden soll, dann kann auch der Driver übergeben werden
        """

        # instanziert den ChromeDriver
        driver = webdriver.Chrome()

        # setzt das Timeout und macht den GET Request an die definierte URL
        driver.set_page_load_timeout(str(self.timeout))
        driver.get(self.url)

        # wählt die checkbox aus und bestätigt diese
        frame = driver.find_element_by_xpath('//iframe[contains(@src, "recaptcha")]')
        driver.switch_to.frame(frame)
        driver.find_element_by_xpath("//*[@id='recaptcha-anchor']").click()

        # warte timeout bis das PopUp gelanden ist
        # time.sleep(self.timeout-5)

        # wählt das PopUp aus und clickt den Audio Button
        popup = driver.find_element(By.XPATH, '/html/body/div[2]/div[4]/iframe')
        driver.switch_to.frame(popup)
        driver.find_element_by_xpath("//*[@id='recaptcha-audio-button']").click()

    def Audio_to_wav(self, mp3Data):
        """
        :param mp3Data: der Pfad\audio.mp3 die zur wav umgewandelt werden soll

        Diese Funktion lädt die ReCaptcha Audio MP3 File, konvertiert sie
        zu einer WAV File und speichert diese in einer Variable zwischen.
        Die WAV File wird in dem gleichen Ordner abgelegt wie der Code, da
        bis jetzt keine vordefinierte Struktur beschlossen wurde.
        """

        audio = AudioSegment.from_mp3(mp3Data)
        audio.export("ConvertetAudio", fromat='wav')

    def Audio_to_text(mp3Data):
        """
        :param mp3Data: der Pfad\audio.mp3 die zur transcripiert werden soll

        Diese Funktion erstellt einen API Request und nutzt die library
        speech_recognition zur übersetzung der Audio-Datei. Der Return ist ein
        String.
        """

        # instanziert die Recognizer-Klasse
        r = sr.Recognizer()

        # instanziert die zu decodierende AudioFile
        encode_audio = sr.AudioFile(mp3Data)

        # instanziert die begrenzt den Nutzen auf encode_audio
        with encode_audio as source:
                audio = r.record(source)

                # print(r.recognize_google(audio))

        return r.recognize_google(audio)

    def String_to_Captcha(self):
        """
        Diese Funktion sendet den transcripierten String aus der AudioFile
        zurück an das ReCaptcha und bestätigt die Eingabe, damit das Captcha
        endgültig gelöst ist
        """

        pass







web = ReCaptchaSlover()
web.get_CaptchaAudio()
