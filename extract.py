import pdfminer.high_level
from pdfminer.layout import LAParams
import glob
import os
import re
import exam

# Set dir_path to current directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# Create empty list of exam objects
exams = []

# Extract and add text from all exam pdfs to examTexts
for filename in glob.glob(f"{dir_path}/Tentor/Pato/*.pdf"):
    # Line below is used for testing or for when only certain exams should be searched
    exams.append(exam.Exam(pdfminer.high_level.extract_text(filename,
                 caching=True, codec='utf-8', laparams=LAParams(line_margin=4)), filename))

# Word(s) to filter questions by
filterWords = [" "]

# Open or create txt file for storing questions
questionsDoc = open(f"Tentafrågor som innehåller {filterWords}.txt","w")

# List all questions containing the specified word and count number of questions
counter = 0
for exam in exams:
    for question in exam.questions:
        for word in filterWords:
            if word.lower() in question.lower():

                # Delete whitespace that might have been accidentally included if question is last on a page
                pagespaceMatch = re.search(r"(\s+[0-9]{1,2}\s*)*$", question)
                if pagespaceMatch:
                    if len(re.search(r"(\s+[0-9]{1,2}\s*)*$", question).group(0)) > 0:
                        question = re.sub(r"(\s+[0-9]{1,2}\s*)*$", "", question)

                # Delete extra tabs caused by bad parsing
                question = re.sub(r"\t", " ", question)

                # Print questions to both terminal and txt file
                print(f"{question}\n")
                questionsDoc.write(question + "\n")
                counter += 1

print(f"\nFound a total of {counter} questions containing {filterWords} \nNumber of exams searched: {len(exams)}\n")

# Tip to remember for later: Codes below represent the symbol for "correct" and "false"
# Rätt = unicode f00c
# Fel = unicode f10c
