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
        self.filename = re.search(r"[^\/]*$", self.path).group(0)

        # Automatic parsing of course name
        class Course:
            def __init__(self, name, termin, searchterm, abbreviation=""):
                self.name = name
                self.termin = termin
                self.searchterm = searchterm
                self.abbreviation = abbreviation

        courses = [
        Course("Molekyl till Vävnad", "T1", "molekyl", "MtV"),
        Course("Rörelse och neurovetenskap", "T2", "rörelse", "RoN"),
        Course("Homeostas", "T3", "homeostas", "HOME"),
        Course("Patogenes", "T4", "pato", "PATO"),
        Course("Klinisk förberedelse", "T5", "förberedelse"),
        Course("Vetenskaplig teori och tillämpning", "T5", "vetenskaplig"),
        Course("Klinisk medicin 1", "T6", "medicin 1", "KM1"),
        Course("Klinisk medicin 2", "T7", "medicin 2", "KM2"),
        Course("Klinisk medicin 3", "T8", "medicin 3", "KM3"),
        Course("Klinisk medicin 4", "T9", "medicin 4", "KM4"),
        Course("Individ och samhälle", "T11", "individ", "IoS"),
        ]

        for course in courses:
            if course.searchterm in self.text[0:80].lower():
                self.course = course.name

        # Parse exam number (ordinary or omtenta)
        if re.search(r"(?<=Kunskapsprov ).", self.path):
            self.number = re.search(r"(?<=Kunskapsprov ).", self.path).group(0)
        elif re.search(r"(?<=Kunskapsprov ).", self.text[0:100]):
            self.number = re.search(r"(?<=Kunskapsprov ).", self.text[0:100]).group(0)
        elif re.search(r"(O|o)rdinarie", self.path):
            self.number = "1"
        elif re.search(r"(O|o)m", self.path) or re.search(r"(O|o)m", self.text[0:100]):
            self.number = "2"
        else:
            self.number = "- oklart (men förmodligen ordinarie prov)"

        # Parse exam semester and year (i.e VTXX or HTXX)
        if re.search(r"(V|H|v|h)(T|t)-? ?[1-2][0-9]", self.path):
            self.semester = re.search(r"(V|H|v|h)(T|t)-? ?[1-2][0-9]", self.path).group(0).upper()
        elif re.search(r"(V|H|v|h)(T|t)-? ?[1-2][0-9]", self.text[0:100]):
            self.semester = re.search(r"(V|H|v|h)(T|t)-? ?[1-2][0-9]", self.text[0:100]).group(0).upper()

        # Split text into questions and remove "Orzone" and "semester" from questions
        if re.search(r"(Q|q)uestion", self.text):
            self.questions = self.text.rsplit("Question")
        elif re.search(r"(F|f)råga", self.text):
            self.questions = re.split(r"(F|f)råga", self.text)
        # Filter out any questions containing "Orzone" and semester from questions
        self.questions = [x for x in self.questions if "Orzone" not in x and self.semester not in x]

        # Fix formatting for questions
        # Remove whitespace and add "question" before number, and add letters for answer alternatives
        for i, question in enumerate(self.questions):
            self.questions[i] = re.sub(r"^\s", f"{self.course} {self.semester}, Prov {self.number} - Fråga ", self.questions[i])
            self.questions[i] = re.sub(r"(\uF00C|\uF10C)", "A", self.questions[i], 1)
            self.questions[i] = re.sub(r"(\uF00C|\uF10C)", "B", self.questions[i], 1)
            self.questions[i] = re.sub(r"(\uF00C|\uF10C)", "C", self.questions[i], 1)
            self.questions[i] = re.sub(r"(\uF00C|\uF10C)", "D", self.questions[i], 1)

# Set dir_path to current directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# Create empty list of exam objects
exams = []

# Extract and add text from all exam pdfs to examTexts
for filename in glob.glob(f"{dir_path}/Tentor/*.pdf"):
    # Line below is used for testing or for when only certain exams should be searched
    #if "Patobiologi 1-tentamen" in filename:
        exams.append(Exam(pdfminer.high_level.extract_text(filename,
                     caching=True, codec='utf-8', laparams=LAParams(line_margin=4)), filename))

# Word(s) to filter questions by
filterWords = ["cancer"]

# Open or create txt file for storing questions
questionsDoc = open(f"Tentafrågor som innehåller {filterWords}.txt","w")

# List all questions containing the specified word and count number of questions
counter = 0
for exam in exams:
    for question in exam.questions:
        for word in filterWords:
            if word.lower() in question.lower():

                # Delete whitespace that might have been accidentally included if question is last on a page
                pagespaceMatch = re.search(r"\s+[1-9][1-9]\s*$", question)
                if pagespaceMatch:
                    if len(re.search(r"\s+[1-9][1-9]\s*$", question).group(0)) > 3:
                        question = re.sub(r"\s+[1-9][1-9]\s*$", "", question)

                # Print questions to both terminal and txt file
                print(f"{question}\n")
                questionsDoc.write(question + "\n")
                counter += 1

print(f"\nFound a total of {counter} questions containing {filterWords} \nNumber of exams searched: {len(exams)}\n")

# Tip to remember for later: Codes below represent the symbol for "correct" and "false"
# Rätt = unicode f00c
# Fel = unicode f10c
