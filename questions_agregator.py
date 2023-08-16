import os
import json


if __name__ == '__main__':
    questions_path = './quiz-questions'
    files = os.listdir(questions_path)
    questions_answers = {}
    for file in files:
        with open(
                f'./quiz-questions/{file}', "r", encoding='KOI8-R'
        ) as my_file:
            file_contents = my_file.read()
    file_items = file_contents.split('\n\n')
    for count, item in enumerate(file_items):
        if 'Вопрос' in item:
            question = item.split(':\n')
            answer = file_items[count + 1].split(':\n')
            questions_answers[question[1]] = answer[1]

    questions_json = json.dumps(questions_answers, ensure_ascii=False)
    with open("questions.json", "w") as my_file:
        my_file.write(questions_json)
