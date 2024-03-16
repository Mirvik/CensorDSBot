from langdetect import detect
from googletrans import Translator

def translate_text(text):
    translator = Translator()
    translated_text = translator.translate(text, dest="en")
    return translated_text.text