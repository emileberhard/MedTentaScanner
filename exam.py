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
        # Remove whitespace and add "question" before number, and add letters for answer alternatives,
        # and if answer alternative letters are lower case, make them upper case.
        for i, question in enumerate(self.questions):
            self.questions[i] = re.sub(r"^\s", f"{self.course} {self.semester}, Prov {self.number} - Fråga ", self.questions[i])
            self.questions[i] = re.sub(r"(\uF00C|\uF10C)", "A", self.questions[i], 1)
            self.questions[i] = re.sub(r"(\uF00C|\uF10C)", "B", self.questions[i], 1)
            self.questions[i] = re.sub(r"(\uF00C|\uF10C)", "C", self.questions[i], 1)
            self.questions[i] = re.sub(r"(\uF00C|\uF10C)", "D", self.questions[i], 1)

            self.questions[i] = re.sub(r"^[abcd]\.", "A", self.questions[i], 1, re.MULTILINE)
            self.questions[i] = re.sub(r"^[abcd]\.", "B", self.questions[i], 1, re.MULTILINE)
            self.questions[i] = re.sub(r"^[abcd]\.", "C", self.questions[i], 1, re.MULTILINE)
            self.questions[i] = re.sub(r"^[abcd]\.", "D", self.questions[i], 1, re.MULTILINE)
