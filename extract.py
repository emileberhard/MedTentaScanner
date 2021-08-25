#!/usr/bin/env python
import glob
import os
import random
import re
import traceback
from exam import Exam
import textract
import argparse

def extract(words, showAnswers):
    # Set dir_path to current directory
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Create empty list of exam objects
    exams = []

    # Extract and add text from all exam pdfs to examTexts
    for filename in glob.glob(f"{dir_path}/Tentor/*.pdf"):
        # Line below is used for testing or for when only certain exams should be searched
        exams.append(Exam(textract.process(filename).decode('utf-8'), filename))
        print(f"Finished scanning {filename}...\n")

    # Word(s) to filter questions by
    filterWords = words

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
                    if showAnswers:
                        print(f"\nRÄTT SVAR: {answerLetter} - {question.answer}")
                    print("\n")
                    counter += 1

    # Print quick scan summary with no. of questions found and exams searched
    print(f"\nFound a total of {counter} questions containing {filterWords} \nNumber of exams searched: {len(exams)}\n")

    while True:
        # Let user check answer of a question
        print("Type a questions number, test and semester to check answer.")

        try:
            checkQNumber = int(input(f"QUESTION NUMBER: ")) - 1
            checkSemester = input("SEMESTER NUMBER (XTYY): ")
            checkTestNo = input("TEST NUMBER (1 or 2): ")

            for exam in exams:
                if checkSemester.upper() == exam.semester and checkTestNo == exam.number:
                    print(f"\nThe answer is: {exam.questions[checkQNumber].answer}\n")
        except:
            print("Invalid entry")
            traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Filter exam questions by filter words')
    parser.add_argument('filterwords',
                           metavar='filterwords',
                           type=str,
                           help='- words to filter by',
                           nargs="+")
    parser.add_argument('-a', action="store_true", help='show answers')

    args = parser.parse_args()
    extract(args.filterwords, args.a)