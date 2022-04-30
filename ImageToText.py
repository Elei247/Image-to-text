# importing modules
import cv2
import pytesseract
from pytesseract import Output

import os, sys, subprocess

# fitz, AKA pymupdf, converts PDFs to text (install pymupdf to use library)
import fitz


# reading image using opencv or pymupdf
image_name = str(input('''
Enter the name of the image from which the text is to be extracted. 
Don't forget to include the extension in the name of the image.  
If the image is not in the same directory as the program, please include the path to the image.
'''))


# Defines whether Windows or Mac OS will be called
def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

# Defines whether a window should be displayed or not, based on user input
def display_window():
    window_input = input("Your text extraction is complete. Do you want to display the text file as a window? Y/N ")
    if (window_input.lower() == "y") or (window_input.lower() == "yes"):
        # Uses open_file function
        open_file("result_text.txt")
    elif (window_input.lower() == "n") or (window_input.lower() == "no"):
        print("Alright. The text document can be found in the same directory as the program.")
    else:
        print("Please type a valid response")

# If the document is an image, openCV will extract the text from the image, adding it to a new text file
if (".jpg" in image_name) or (".png" in image_name) or (".jpeg" in image_name):
    image = cv2.imread(image_name)

    #converting image into gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # converting it to binary image by Thresholding
    # this step is require if you have colored image because if you skip this part
    # then tesseract won't able to detect text correctly and this will give incorrect result
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # display image
    print('Displaying a black and white version of the image so the text is more easily visible...')
    cv2.imshow('threshold image', threshold_img)

    # Maintain output window for 5 seconds
    cv2.waitKey(5000)

    # Destroying present windows on screen
    cv2.destroyAllWindows()

    #configuring parameters for tesseract

    custom_config = r'--oem 3 --psm 6'

    # now feeding image to tesseract

    details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='eng')

    total_boxes = len(details['text'])

    for sequence_number in range(total_boxes):

        if float(details['conf'][sequence_number]) >30:
            (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
            threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # display image
    print('highlighting detected texts in the image...')
    cv2.imshow('captured text', threshold_img)

    # Maintain output window for 5 seconds

    cv2.waitKey(5000)

    # Destroying present windows on screen

    cv2.destroyAllWindows()

    parse_text = []

    word_list = []

    last_word = ''

    for word in details['text']:

        if word!='':

            word_list.append(word)

            last_word = word

        if (last_word!='' and word == '') or (word==details['text'][-1]):

            parse_text.append(word_list)

            word_list = []
        
    import csv

    with open('result_text.txt',  'w', newline="") as file:

        csv.writer(file, delimiter=" ").writerows(parse_text)

    display_window()

# This opens the PDF document and extracts the text, adding it to a new text file
elif (".pdf" in image_name):
    with fitz.open(str(image_name)) as pdf:
        with open('pdf-extract.txt',  'w') as pdf_extract:
            text = ""
            for page in pdf:
                text += page.get_text()
                text += "\n"
        
            pdf_extract.write(str(text))

    display_window()

else:
    print("Type a valid file type: .pdf, .png, .jpeg or .jpg!")
