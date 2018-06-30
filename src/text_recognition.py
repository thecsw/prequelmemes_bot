import urllib
import os, sys
import pytesseract
import cv2
from PIL import Image

def check_size(filename):
    os_stat = os.stat(filename)
    size = os_stat.st_size
    # If the file size exceeds 10 MB, skip the file
    if ((size / 1000) > 10 * 1000):
        return False
    return True

def extract_image(post):

    """
    This function extracts an image from a reddit post and saves it as 'temp'.
    For some reason different distros behave differently with urllib
    Arch linux uses urllib.request.urlretrieve()
    Debian and Ubuntu distros use urllib.urlretrieve
    """
    # We would just call all the temporary images as "temp"
    meme_name = "temp"          
    
    try:
        # Here we are downloading the appropriate image (png, jpg, jpeg, bmp)
        urllib.urlretrieve(post.url, filename=meme_name) 
    except:
        urllib.request.urlretrieve(post.url, filename=meme_name)

    return meme_name
        
def text_recognition(meme_name):

    if (check_size(meme_name)):
        os.remove(meme_name)
        return False
    
    # We load up the image using opencv
    image = cv2.imread(meme_name)                    

    # Turning the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    # Making a threshold for the image, text will be more apparent
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] 

    # Adding some blur, useful for really noisy images
    gray = cv2.medianBlur(gray, 3) 

    # Making the temporary, ready file for text recognition
    filename = "{}-ocr.png".format(meme_name) 

    # Now, we will save the image
    cv2.imwrite(filename, gray)

    # Open the processed image with pillow
    img = Image.open(filename)

    # As a means of exceptions, need to read out as UTF-8, so no encoding errors would occur
    recognized_text = pytesseract.image_to_string(img).encode('utf-8') 
    os.remove(filename)
    os.remove(meme_name)

    # Returns the recognized text in UTF-8 encodign and with capital and lower letters
    return recognized_text
