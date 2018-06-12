import urllib
import os, sys
import pytesseract
import cv2
from PIL import Image

def extract_image(post):
    meme_name = "temp"          # We would just call all the temporary images as "temp"
    try:
        urllib.urlretrieve(post.url, filename=meme_name) # Here we are downloading the appropriate image (png, jpg, jpeg, bmp)
    except:
        urllib.request.urlretrieve(post.url, filename=meme_name)
    return meme_name
        
def text_recognition(image_name):

    # For some reason different distros behave differently with urllib
    # Arch linux uses urllib.request.urlretrieve()
    # Debian and Ubuntu distros use urllib.urlretrieve
        
    image = cv2.imread(meme_name)                    # We load up the image using opencv
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Turning the image to grayscale
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] # Making a threshold for the image, text will be more apparent
    gray = cv2.medianBlur(gray, 3) # Adding some blur, useful for really noisy images
    filename = "{}-ocr.png".format(meme_name) # Making the temporary, ready file for text recognition
    cv2.imwrite(filename, gray)               # Now, we will save the image
    img = Image.open(filename)                # Open the processed image with pillow
    recognized_text = pytesseract.image_to_string(img).encode('utf-8') # As a means of exceptions, need to read out as UTF-8, so no encoding errors would occur
    os.remove(filename)
    os.remove(meme_name)
    return recognized_text      # Returns the recognized text in UTF-8 encodign and with capital and lower letters
