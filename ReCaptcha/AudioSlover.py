# Import the base64 encoding library.
import speech_recognition as sr
from pydub import AudioSegment
import os


def to_wav():
    ''' Diese Funktion lädt die ReCaptcha Audio MP3 File, konvertiert sie
        zu einer WAV File und speichert diese in einer Variable zwischen. '''

    audio = AudioSegment.from_mp3("audio.mp3")
    audio.export("buum.wav", fromat='wav')




def to_text():

        # instanziert die Recognizer-Klasse
        r = sr.Recognizer()

        # instanziert die zu decodierende AudioFile
        encode_audio = sr.AudioFile('audio.mp3')

        # instanziert die begrenzt den Nutzen auf encode_audio
        with encode_audio as source:
                audio = r.record(source)

                print(r.recognize_google(audio))



to_wav()
