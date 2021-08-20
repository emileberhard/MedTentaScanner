import pdfminer.high_level
from pdfminer.layout import LAParams
import glob
import os

# Set dir_path to current directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# Create empy text strings
text = ""

# Extract and add text from all exams into one string (text)
for filename in glob.glob(f"{dir_path}/*.pdf"):
    text += pdfminer.high_level.extract_text(filename,
                     caching=True, codec='utf-8', laparams=LAParams(line_margin=4))

# Tip: Cdes below represent the symbol for "correct" and "false"
# Rätt = unicode f00c
# Fel = unicode f10c

# Prints the unfiltered extracted text
#print(text)

# Create a list with the questions (without "Orzone AB" "questions") as strings and prints
questionsUnfiltered = text.rsplit("Question")
questions = [x for x in questionsUnfiltered if "Orzone" not in x and "VT-21" not in x]

for question in questions:
    if "citrat" in question or "Citrat" in question:
        print(f"{question}")
