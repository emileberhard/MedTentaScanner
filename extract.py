#!/usr/bin/env python
import glob
import os
import random
import re
import traceback
from exam import Exam
import textract
import argparse
from time import sleep
import sys

# Create parser
parser = argparse.ArgumentParser(description='Filter exam questions by filter words')

# Filter words
parser.add_argument('filterwords',
                           metavar='filterwords',
                           type=str,
                           help='- words to filter by',
                           nargs="+")

# Optional flags
parser.add_argument('-a', action="store_true", help='show answers')
parser.add_argument('-q', action="store_true", help='quiz mode')

# Create args variable
args = parser.parse_args()

def extract(words, showAnswers):
    # Set dir_path to current directory
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Create empty list of exam objects
    exams = []

    # Extract and add text from all exam pdfs to examTexts
    for filename in glob.glob(f"{dir_path}/Tentor/*.pdf"):
        # Line below is used for testing or for when only certain exams should be searched
        exams.append(Exam(textract.process(filename, method="pdftotext").decode('utf-8'), filename))
        print(f"Finished scanning {filename}...\n")

    # Word(s) to filter questions by
    filterWords = words

    resultDoc = open(f"Previous searches/Tentafrågor som innehåller {filterWords}.html", "w")
    resultDoc.write("<meta charset=\"UTF-8\">")
    resultDoc.write("<style>body {background-color: linen;font-family: Arial, Helvetica, sans-serif;} </style>")
    resultDoc.close()

    answerDoc = open(f"Previous searches/Tentafrågor som innehåller {filterWords} FACIT.html", "w")
    answerDoc.write("<meta charset=\"UTF-8\">")
    answerDoc.write("<style>"
                    "body {background-color: linen;font-family: Arial, Helvetica, sans-serif;} "
                    ""
                    "</style>")
    answerDoc.write("<h1 style=\"font-size:70px\">FACIT</h1>")
    answerDoc.close()

    # List all questions containing the specified word and count number of questions
    counter = 0
    for exam in exams:
        for question in exam.questions:
            for word in filterWords:
                if word.lower() in question.text.lower():
                    # Print questions to both terminal and result file
                    print(f"{question.title}\n{question.question}")
                    resultDoc = open(f"Previous searches/Tentafrågor som innehåller {filterWords}.html", "a")
                    resultDoc.write(f"<b><u>{question.title}</b></u><br>{question.question}")
                    resultDoc.close()
                    answerDoc = open(f"Previous searches/Tentafrågor som innehåller {filterWords} FACIT.html","a")
                    answerDoc.write(f"<b><u>{question.title}</b></u><br>{question.question}")
                    answerDoc.close()

                    # Shuffle answer alternatives
                    keys = list(question.answerAlternatives.keys())
                    random.shuffle(keys)

                    # Print answer alternatives
                    i = 0
                    answerAltLetters = ["A", "B", "C", "D"]
                    for ansAlt in keys:
                        answer = False
                        if question.answer == question.answerAlternatives[ansAlt]:
                            answerLetter = answerAltLetters[i]
                            answer = True

                        print(f"\n{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}")
                        if answer and showAnswers:
                            resultDoc = open(f"Previous searches/Tentafrågor som innehåller {filterWords}.html", "a")
                            resultDoc.write(f"<br><br><b>{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}</b>")
                            resultDoc.close()
                            answerDoc = open(f"Previous searches/Tentafrågor som innehåller {filterWords} FACIT.html",
                                             "a")
                            answerDoc.write(
                                f"<br><br><b>{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}</b>")
                            answerDoc.close()
                        elif answer:
                            resultDoc = open(f"Previous searches/Tentafrågor som innehåller {filterWords}.html", "a")
                            resultDoc.write(f"<br><br>{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}")
                            resultDoc.close()
                            answerDoc = open(f"Previous searches/Tentafrågor som innehåller {filterWords} FACIT.html","a")
                            answerDoc.write(f"<br><br><b>{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}</b>")
                            answerDoc.close()
                        else:
                            resultDoc = open(f"Previous searches/Tentafrågor som innehåller {filterWords}.html", "a")
                            resultDoc.write(f"<br><br>{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}")
                            resultDoc.close()
                            answerDoc = open(f"Previous searches/Tentafrågor som innehåller {filterWords} FACIT.html","a")
                            answerDoc.write(f"<br><br>{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}")
                            answerDoc.close()

                        i += 1

                    # Print answer if show answers flag was used
                    if showAnswers:
                        print(f"\nRÄTT SVAR: {answerLetter} - {question.answer}")

                    print("\n")
                    resultDoc = open(f"Previous searches/Tentafrågor som innehåller {filterWords}.html", "a")
                    resultDoc.write("<br><br><br>")
                    resultDoc.close()
                    answerDoc = open(f"Previous searches/Tentafrågor som innehåller {filterWords} FACIT.html","a")
                    answerDoc.write(f"<br><br><br>")
                    answerDoc.close()
                    counter += 1

    # Print quick scan summary with no. of questions found and exams searched
    print(f"\nFound a total of {counter} questions containing {filterWords} \nNumber of exams searched: {len(exams)}\n")
    if showAnswers:
        os.remove(f"Previous searches/Tentafrågor som innehåller {filterWords} FACIT.html")
        print("removed facit")
    while True:
        # Let user check answer of a question
        print("You can check the answer for a question, or type \"quit\" to exit:")

        try:
            checkQNumber = input("QUESTION NUMBER (\"quit\" to exit): ")
            if checkQNumber == "quit":
                break
            checkSemester = input("SEMESTER NUMBER (XTYY): ")
            checkTestNo = input("TEST NUMBER (1 or 2): ")

            for exam in exams:
                for question in exam.questions:
                    if question.number == checkQNumber:
                        print(f"\nThe answer is: {question.answer}\n")
                        sleep(2)

        except:
            print("Invalid entry")
            traceback.print_exc()

if __name__ == "__main__":
    extract(args.filterwords, args.a)
