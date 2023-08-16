import os
import json
from environs import Env


if __name__ == '__main__':
    env = Env()
    env.read_env()

    questions_path = env.str('QUESTIONS_PATH', './quiz-questions')
    files = os.listdir(questions_path)
    questions_answers = {}
    for file in files:
        with open(
                f'{questions_path}{file}', "r", encoding='KOI8-R'
        ) as questions:
            file_contents = questions.read()
    file_items = file_contents.split('\n\n')
    for count, item in enumerate(file_items):
        if 'Вопрос' in item:
            question = item.split(':\n')
            answer = file_items[count + 1].split(':\n')
            questions_answers[question[1]] = answer[1]

    questions_json = json.dumps(questions_answers, ensure_ascii=False)
    with open("questions.json", "w") as questions:
        questions.write(questions_json)
