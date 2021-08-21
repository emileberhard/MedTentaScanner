import pdfminer.high_level
from pdfminer.layout import LAParams
import glob
import os
import re

class Exam:
    def __init__(self, text, path):
        # Add text to text string
        self.text = text

        # Add file path to path string
        self.path = path

        # Parse exam info
        self.number = re.search(r"(?<=Kunskapsprov ).", self.path).group(0)
        self.semester = re.search(r"(V|H|v|h)T-? ?[1-2][0-9]", self.path).group(0)

        # Split text into questions and remove "Orzone" and "semester" from questions
        self.questions = self.text.rsplit("Question")
        self.questions = [x for x in self.questions if "Orzone" not in x and self.semester not in x]

        # Fix formatting for questions
        # Remove whitespace and add "question" before number, and add letters for answer alternatives
        for i, question in enumerate(self.questions):
            self.questions[i] = re.sub(r"^\s", f"{self.semester}, Prov {self.number}, Fråga ", self.questions[i])
            self.questions[i] = re.sub(r"(\uF00C|\uF10C)", "A", self.questions[i], 1)
            self.questions[i] = re.sub(r"(\uF00C|\uF10C)", "B", self.questions[i], 1)
            self.questions[i] = re.sub(r"(\uF00C|\uF10C)", "C", self.questions[i], 1)
            self.questions[i] = re.sub(r"(\uF00C|\uF10C)", "D", self.questions[i], 1)

        # Add automatic parsing for these later
        self.course = None


# Set dir_path to current directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# Create empty list of exam objects
exams = []

# Extract and add text from all exam pdfs to examTexts
for filename in glob.glob(f"{dir_path}/*.pdf"):
    exams.append(Exam(pdfminer.high_level.extract_text(filename,
                     caching=True, codec='utf-8', laparams=LAParams(line_margin=4)), filename))

# Word(s) to filter questions by
filterWords = ["cyklin", "Cdk", "CKI"]

# Open or create txt file for storing questions
questionsDoc = open(f"Tentafrågor som innehåller {filterWords}.txt","w")

# List all questions containing the specified word and count number of questions
counter = 0
for exam in exams:
    for question in exam.questions:
        for word in filterWords:
            if word.lower() in question.lower():
                print(f"{question}")
                questionsDoc.write(question)
                counter += 1

print(f"\nFound a total of {counter} questions containing {filterWords} \nNumber of exams searched: {len(exams)}\n")



# Tip to remember for later: Codes below represent the symbol for "correct" and "false"
# Rätt = unicode f00c
# Fel = unicode f10c
