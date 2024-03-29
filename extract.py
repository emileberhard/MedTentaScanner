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
from collections import Counter

# Create parser
parser = argparse.ArgumentParser(description='Filter exam questions by filter words')

# Filter words
parser.add_argument('filterwords', type=str, help='- words to filter by', nargs="+")

# Optional flags
parser.add_argument('-a', action="store_true", help='show answers')
parser.add_argument('-c', action="store_true", help='enables answer checking search tool')
parser.add_argument('-q', action="store_true", help='quiz mode')

# Create args variable
args = parser.parse_args()


def main(filterwords =args.filterwords):
    exams = extract()
    searchresult = search(filterwords, exams)
    output(searchresult, filterwords)
    totalquestions = numquestions(exams)
    # Print quick scan summary with no. of questions found and exams searched
    print(f"Found a total of {len(searchresult)} (out of {totalquestions}) questions containing {filterwords} \n"
          f"Number of exams searched: {len(exams)}\n")

    if args.c:
        checkanswer(exams)

    while True:
        newsearch = input("Search for another word or words (or type \"quit\" to quit): ")
        print("\n")
        if newsearch == "quit":
            quit()
        else:
            newwords = newsearch.split(" ")
            main(newwords)


def examswordfreq(exams):
    joinedrext = ""
    for exam in exams:
        joinedrext += exam.text

    allwords = re.findall(r"\b[^\s]+\b", joinedrext)

    wordsfreq = Counter(allwords)

    return wordsfreq


def answerwordfreq(exams):
    joinedanswers = ""
    for exam in exams:
        for question in exam.questions:
            joinedanswers += question.answer

    allwords = re.findall(r"\b[^\s]+\b", joinedanswers)

    wordsfreq = Counter(allwords)

    return wordsfreq


def numquestions(exams):
    # Simple function to count number of questions in exams
    number = 0
    for exam in exams:
        for question in exam.questions:
            number += 1
    return number


def extract():
    # Set dir_path to current directory
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Create empty list of exam objects
    extractedexams = []

    # Extract and add text from all exam pdfs to examTexts
    for filename in glob.glob(f"{dir_path}/Tentor/*.pdf"):
        # Line below is used for testing or for when only certain exams should be searched
        extractedexams.append(Exam(textract.process(filename, method="pdftotext").decode('utf-8'), filename))
        print(f"Finished scanning {filename}...\n")

    return extractedexams


def search(words, exams):
    # List all questions containing the specified word and count number of questions
    wordfilter = words
    searchresult = []

    for exam in exams:
        for question in exam.questions:
            for word in wordfilter:
                if word.lower() in question.text.lower():
                    searchresult.append(question)

    return searchresult


def output(questions, words):

    # Word(s) to filter questions by
    filterWords = words

    resultDoc = open(f"Searches/Tentafrågor som innehåller {filterWords}.html", "w")
    resultDoc.write("<meta charset=\"UTF-8\">")
    resultDoc.write("<style>body {background-color: linen;font-family: Arial, Helvetica, sans-serif;} </style>")
    resultDoc.close()

    answerDoc = open(f"Searches/Tentafrågor som innehåller {filterWords} FACIT.html", "w")
    answerDoc.write("<meta charset=\"UTF-8\">")
    answerDoc.write("<style>"
                    "body {background-color: linen;font-family: Arial, Helvetica, sans-serif;} "
                    ""
                    "</style>")
    answerDoc.write("<h1 style=\"font-size:70px\">FACIT</h1>")
    answerDoc.close()

    for question in questions:
        # Print questions to both terminal and result file
        print(f"{question.title}\n{question.question}")
        resultDoc = open(f"Searches/Tentafrågor som innehåller {filterWords}.html", "a")
        resultDoc.write(f"<b><u>{question.title}</b></u><br>{question.question}")
        resultDoc.close()
        answerDoc = open(f"Searches/Tentafrågor som innehåller {filterWords} FACIT.html", "a")
        answerDoc.write(f"<b><u>{question.title}</b></u><br>{question.question}")
        answerDoc.close()

        # Shuffle answer alternatives
        keys = list(question.answerAlternatives.keys())
        random.shuffle(keys)

        # Print answer alternatives
        i = 0
        answerAltLetters = ["A", "B", "C", "D"]
        answerLetter = ""
        for ansAlt in keys:
            answer = False
            if question.answer == question.answerAlternatives[ansAlt]:
                answerLetter = answerAltLetters[i]
                answer = True

            print(f"\n{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}")
            if answer and args.a:
                resultDoc = open(f"Searches/Tentafrågor som innehåller {filterWords}.html", "a")
                resultDoc.write(f"<br><br><b>{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}</b>")
                resultDoc.close()
                answerDoc = open(f"Searches/Tentafrågor som innehåller {filterWords} FACIT.html",
                                 "a")
                answerDoc.write(
                    f"<br><br><b>{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}</b>")
                answerDoc.close()
            elif answer:
                resultDoc = open(f"Searches/Tentafrågor som innehåller {filterWords}.html", "a")
                resultDoc.write(f"<br><br>{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}")
                resultDoc.close()
                answerDoc = open(f"Searches/Tentafrågor som innehåller {filterWords} FACIT.html", "a")
                answerDoc.write(f"<br><br><b>{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}</b>")
                answerDoc.close()
            else:
                resultDoc = open(f"Searches/Tentafrågor som innehåller {filterWords}.html", "a")
                resultDoc.write(f"<br><br>{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}")
                resultDoc.close()
                answerDoc = open(f"Searches/Tentafrågor som innehåller {filterWords} FACIT.html", "a")
                answerDoc.write(f"<br><br>{answerAltLetters[i]}: {question.answerAlternatives[ansAlt]}")
                answerDoc.close()

            i += 1

        # Print answer if show answers flag was used
        if args.a:
            print(f"\nRÄTT SVAR: {answerLetter} - {question.answer}")

        print("\n")
        resultDoc = open(f"Searches/Tentafrågor som innehåller {filterWords}.html", "a")
        resultDoc.write("<br><br><br>")
        resultDoc.close()
        answerDoc = open(f"Searches/Tentafrågor som innehåller {filterWords} FACIT.html", "a")
        answerDoc.write(f"<br><br><br>")
        answerDoc.close()

    if args.a:
        os.remove(f"Searches/Tentafrågor som innehåller {filterWords} FACIT.html")


def category(exams, category):
    Cellcykeln = ["cyklin"]
    print("d")


def checkanswer(exams):
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
                if exam.semester == checkSemester and exam.number == checkTestNo:
                    for question in exam.questions:
                        if question.number == checkQNumber:
                            print(f"\nThe answer is: {question.answer}\n")
                            sleep(2)

        except:
            print("Invalid entry")
            traceback.print_exc()


if __name__ == "__main__":
    main()
