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

        # Fix formatting for questions (remove whitespace and add "question" before no.)
        for i, question in enumerate(self.questions):
            self.questions[i] = re.sub(r"^\s", f"{self.semester}, Prov {self.number}, Fråga ", question)

        # Add automatic parsing for these later
        self.course = None


dir_path = os.path.dirname(os.path.realpath(__file__))

exams = []

for filename in glob.glob(f"{dir_path}/*.pdf"):
    exams.append(Exam("VT21 Question 5 testfråga", filename))

print(exams[0].semester + "\n")
print(exams[0].questions[1] + "\n")
print(exams[4].number + "\n")
