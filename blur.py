import re
import detection
from langdetect import detect
from googletrans import Translator
from allowedCategories import AllowedCategories

def blur_word(text):
 
    def childrenFn(text, target_word):
        original_language = detect(text)

        translator = Translator()
        translated_target_word = translator.translate(target_word, src="en", dest=original_language).text

        blurred_text = re.sub(rf'{translated_target_word}', lambda match: '#' * len(match.group()), text, flags=re.IGNORECASE)

        return blurred_text
 
    for target_word in target_words:
        text = childrenFn(text, target_word  )
        
    return text


def blur(text):

    hate_detections = detection.f(translate_text(text.lower()))

    arr_bad_word = []
    allowed_categories = AllowedCategories(set())

    toBlur = allowed_categories.filterWords(hate_detections[1]) 
    print(toBlur)

    if (len(toBlur) != 0):
        for word_and_category in toBlur:
            arr_bad_word.append(word_and_category[0])