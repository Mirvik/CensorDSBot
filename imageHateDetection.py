import pytesseract
from PIL import Image, ImageFilter
import requests
from io import BytesIO
import detection

pytesseract.pytesseract.tesseract_cmd = r"E:\Tesseract\tesseract.exe"

def get_text_and_coordinates(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    textData = []
    for i, word in enumerate(data['text']):
        if word.strip():
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            coordinates = (x, y, x + w, y + h)  # (left, top, right, bottom)
            textData.append([word, coordinates])

    return image, textData

def blurBadWords(image: Image, wordsToBlur):
    for tD in wordsToBlur:
        croppedImage = image.crop(tD[1])

        blurredImage = croppedImage.filter(ImageFilter.GaussianBlur(radius=5))
        image.paste(blurredImage, tD[1])

    return image



def redactImage(url) -> Image:
    image, textData = get_text_and_coordinates(url)

    fullText = ""
    for t in textData:
        fullText += f'{t} '

    detectedHate = detection.f(fullText)

    wordsToBlur = []
    for badWord in detectedHate[1]:
        for tD in textData:
            if tD[0] == badWord[0]:
                wordsToBlur.append(tD)
                break

    resImage = blurBadWords(image, wordsToBlur)

    return resImage

image = redactImage('https://onlinejpgtools.com/images/examples-onlinejpgtools/trap-with-text.jpg')
image2 = redactImage('https://i.ytimg.com/vi/_pxXx2O9Ojc/maxresdefault.jpg')
#with BytesIO() as image_binary:
#    image.save(image_binary, 'PNG')
#    image_binary.seek(0)

#pip insall -r req.txt