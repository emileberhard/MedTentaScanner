import re

#Class for exams
class Exam:

    # Inner class for courses
    class Course:
        def __init__(self, name, termin, searchterm, abbreviation=""):
            self.name = name
            self.termin = termin
            self.searchterm = searchterm
            self.abbreviation = abbreviation

    # Make a static list with all medicine courses (at Lund Uni)
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
    # Keeps going... But is folded to take less space

    # Class for questions - to keep track of question, answer alternatives,
    # and store correct answer
    class Question:
        def __init__(self, text, exam):
            self.text = text
            self.exam = exam

            # Add question number to number variable (before doing anything else to self.text)
            self.number = re.search(r"\d{1,3}", self.text).group(0)
            # Remove question number from self.text
            self.text = re.sub(r"\d{1,3}", "", self.text, 1)

            ### FIX FORMATTING FOR QUESTIONS ###
            # Add a "title" to the question
            self.text = re.sub(r"^\s", f"{self.exam.course.name} {self.exam.semester}, Prov {self.exam.number} - Fråga {self.number}", self.text)

            # Remove whitespace and add "question" before number, and add letters for answer alternatives,
            self.text = re.sub(r"(\uF00C|\uF10C)", "A", self.text, 1)
            self.text = re.sub(r"(\uF00C|\uF10C)", "B", self.text, 1)
            self.text = re.sub(r"(\uF00C|\uF10C)", "C", self.text, 1)
            self.text = re.sub(r"(\uF00C|\uF10C)", "D", self.text, 1)

            # If answer alternative letters already exist but are lower case, make them upper case.
            self.text = re.sub(r"^[abcd]\.", "A", self.text, 1, re.MULTILINE)
            self.text = re.sub(r"^[abcd]\.", "B", self.text, 1, re.MULTILINE)
            self.text = re.sub(r"^[abcd]\.", "C", self.text, 1, re.MULTILINE)
            self.text = re.sub(r"^[abcd]\.", "D", self.text, 1, re.MULTILINE)

            # Delete whitespace that might have been accidentally included if question is last on a page
            pagespaceMatch = re.search(r"(\s+[0-9]{1,2}\s*)*$", self.text)
            if pagespaceMatch:
                if len(re.search(r"(\s+[0-9]{1,2}\s*)*$", self.text).group(0)) > 0:
                    self.text = re.sub(r"(\s+[0-9]{1,2}\s*)*$", "", self.text)

            # Delete extra tabs caused by bad parsing
            self.text = re.sub(r"\t", " ", self.text)

            # Isolate the actual question part of the
            self.question = re.search(r".*(?=^A)", self.text, flags=re.MULTILINE | re.DOTALL).group(0)
            self.question = re.search(r".*\S", self.question).group(0)

            # Parse answer alternatives
            self.answerAlternatives = re.sub(r".*(?=^A)", "", self.text, flags=re.MULTILINE | re.DOTALL)

    def __init__(self, text, path):
        # Add text to text string
        self.text = text

        # Add file path to path string
        self.path = path
        self.filename = re.search(r"[^\/]*$", self.path).group(0)

        # Automatic parsing of course name
        for course in self.courses:
            if course.searchterm in self.text[0:80].lower():
                self.course = course

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
        if re.search(r"(V|H|v|h)(T|t)-? ?[1-2][0-9]", self.filename):
            self.semester = re.search(r"(V|H|v|h)(T|t)-? ?[1-2][0-9]", self.filename).group(0).upper()
        elif re.search(r"(V|H|v|h)(T|t)-? ?[1-2][0-9]", self.text[0:100]):
            self.semester = re.search(r"(V|H|v|h)(T|t)-? ?[1-2][0-9]", self.text[0:100]).group(0).upper()

        # Split text into questions
        if re.search(r"(Q|q)uestion", self.text):
            self.rawQuestions = self.text.rsplit("Question")
        elif re.search(r"(F|f)råga", self.text):
            self.rawQuestions = re.split(r"(?:F|f)råga(?=\s)", self.text)

        #Debug
        # Need to make it so that the parser removes Orzone endings from real questions
        # and also removes Orzone-only questions without removing real questions
        print(f"\nFound a total of {len(self.rawQuestions)} questions BEFORE FORMATTING\n")
        #Debug

        # FILTERING OUT FAKE QUESTIONS
        # Filter out any questions containing only "Orzone..."
        self.rawQuestions = [x for x in self.rawQuestions if not
                            re.search(r"^(?<!\w)\s*\d*\s*Orzone\s*AB\s*Gothenburg\s*www\.orzone\.com.*$", x, flags=re.IGNORECASE|re.DOTALL)]
        # Filter out questions containing a question, but with an "Orzone.. at the end"
        self.rawQuestions = [re.sub(r"\s*Orzone\s*AB\s*Gothenburg\s*www\.orzone\.com\s*\+?\s*$", "", x) for x in self.rawQuestions]
        # Filter out any questions containing semester (1st "question") and course name from questions
        self.rawQuestions = [x for x in self.rawQuestions if not
                            re.search(rf"^(?=.*(h|v)t-?\d\d\D)(?=.*{self.course.searchterm}).*$", x, flags=re.IGNORECASE|re.DOTALL)]

        #Debug
        print(f"\nFound a total of {len(self.rawQuestions)} questions AFTER INITIAL FORMATTING\n")
        #Debug




        # Make a list of question objects using the questions extracted using split
        self.questions = []
        for question in self.rawQuestions:
            self.questions.append(self.Question(question, self))
