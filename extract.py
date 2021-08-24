import glob
import os
import random

import exam
import textract

# Set dir_path to current directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# Create empty list of exam objects
exams = []

# Extract and add text from all exam pdfs to examTexts
for filename in glob.glob(f"{dir_path}/Tentor/*.pdf"):
    # Line below is used for testing or for when only certain exams should be searched
    exams.append(exam.Exam(textract.process(filename).decode('utf-8'), filename))
    print(f"Finished scanning {filename}...\n")

# Word(s) to filter questions by
filterWords = ["cyklin"]

# Open or create txt file for storing questions
questionsDoc = open(f"Arkiv/Tentafrågor som innehåller {filterWords}.txt", "w")

# List all questions containing the specified word and count number of questions
counter = 0
for exam in exams:
    for question in exam.questions:
        for word in filterWords:
            if word.lower() in question.text.lower():
                # Print questions to both terminal and txt file
                print(f"{question.title}\n{question.question}")

                # Shuffle answer alternatives
                keys = list(question.answerAlternatives.keys())
                random.shuffle(keys)

                # Print answer alternatives
                i = 0
                answerAltLetters = ["A", "B", "C", "D"]
                for ansAlt in keys:
                    print(f"\n{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}")
                    if question.answer in question.answerAlternatives[ansAlt]:
                        answerLetter = answerAltLetters[i]
                    i += 1

                print(f"\nRÄTT SVAR: {answerLetter} - {question.answer}")
                print("\n")
                #questionsDoc.write(question.text + "\n")
                counter += 1

# Print quick scan summary with no. of questions found and exams searched
print(f"\nFound a total of {counter} questions containing {filterWords} \nNumber of exams searched: {len(exams)}\n")

# Tip to remember for later: Codes below represent the symbol for "correct" and "false"
# Rätt = unicode f00c
# Fel = unicode f10c
