import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import logging
from environs import Env
import random
import json
import redis

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    env = Env()
    env.read_env()
    vk_token = env.str('VK_TOKEN')
    questions_file = env.str('PATH_QUESTIONS_FILE', './questions.json')
    redis_host = env.str('REDIS_HOST')
    redis_port = env.str('REDIS_PORT')
    redis_pass = env.str('REDIS_PASS')
    language_code = 'ru-RU'

    pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=0,
                                password=redis_pass)
    redis_connect = redis.Redis(connection_pool=pool)

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.SECONDARY)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == "Сдаться":
                question = redis_connect.get(event.user_id).decode(
                    'utf-8')
                with open(questions_file) as questions:
                    questions = json.loads(questions.read())
                    answer = questions[question]
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=f'Верный ответ: {answer}'
                            f'\nЧто бы продолжить, нажми "Новый вопрос"',
                    random_id=random.randint(1, 1000),
                    keyboard=keyboard.get_keyboard()
                )
            elif event.text == "Новый вопрос":
                with open(questions_file) as questions:
                    questions = json.loads(questions.read())
                    question = random.choice(list(questions))
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=question,
                    random_id=random.randint(1, 1000),
                    keyboard=keyboard.get_keyboard()
                )
                redis_connect.set(event.user_id, question)
            else:
                question = redis_connect.get(event.user_id).decode(
                    'utf-8')
                with open(questions_file) as questions:
                    questions = json.loads(questions.read())
                    answer = questions[question].split('.')[0]
                    if event.text == answer:
                        vk_api.messages.send(
                            user_id=event.user_id,
                            message='Верно'
                                    'Что бы продолжить, нажми "Новый вопрос"',
                            random_id=random.randint(1, 1000),
                            keyboard=keyboard.get_keyboard()
                        )
                    else:
                        vk_api.messages.send(
                            user_id=event.user_id,
                            message='Не верно'
                                    'Что бы продолжить, нажми "Новый вопрос"',
                            random_id=random.randint(1, 1000),
                            keyboard=keyboard.get_keyboard()
                        )
