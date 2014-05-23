#! /usr/bin/python

import time
import os
import sys
import random

BASE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
N_QUESTIONS = 5

log_file = open(BASE_DIR + '/errors.log', 'a')

completed = False
questions = []


def say_wake_up():
    os.system('say "wake up"')


def write_out_questions():
    global questions
    questions = [(int(random.random() * 100), int(random.random() * 100))
                 for i in range(N_QUESTIONS)]
    with open(BASE_DIR + '/questions.txt', 'w') as question_file:
        for question in questions:
            question_file.write('%d * %d\n' % (question[0], question[1]))

write_out_questions()


def error(msg):
    log_file.write(msg + '\n')
    log_file.flush()


def is_answer_to_question(question, answer):
    try:
        return question[0] * question[1] == int(answer)
    except ValueError:
        error('caught value error converting %s to int' % answer)
        return False


def check_completed():
    global completed
    answer_file = BASE_DIR + '/answers.txt'
    if not os.path.exists(answer_file):
        return

    with open(answer_file) as answers_file:
        answers = [answer_line.strip() for answer_line in answers_file]
        if len(answers) != len(questions):
            error('number of answers is not equal to the number of questions')
            return

        for question, answer in zip(questions, answers):
            if not is_answer_to_question(question, answer):
                error('wrong answer %s to question %s'
                      % (answer, question))
                return

    completed = True

while not completed:
    say_wake_up()
    check_completed()
    time.sleep(2)

log_file.close()
