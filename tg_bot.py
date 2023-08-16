import logging
import json
import random
import redis
from environs import Env
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackContext, ConversationHandler)

# Enable logging
logger = logging.getLogger(__name__)

QUESTION, CHECK_QUESTION_ANSWER = range(2)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_markdown_v2(
        fr'Привет, {user.mention_markdown_v2()}\!'
        fr' Я бот для викторин\!',
        reply_markup=reply_markup
    )


def handle_new_question_request(
        update: Update, context: CallbackContext, redis_connect, questions_file
) -> None:
    with open(questions_file) as questions:
        questions = json.loads(questions.read())
        question = random.choice(list(questions))
        update.message.reply_text(question)
        redis_connect.set(update.effective_chat.id, question)
    return CHECK_QUESTION_ANSWER


def handle_solution_attempt(
        update: Update, context: CallbackContext, redis_connect, questions_file
):
    question = redis_connect.get(update.effective_chat.id).decode('utf-8')
    with open(questions_file) as questions:
        questions = json.loads(questions.read())
        answer = questions[question].split('.')[0]
        if update.message.text == answer:
            update.message.reply_text(
                'Верно. Что бы продолжить, нажми "Новый вопрос"'
            )
        else:
            update.message.reply_text(
                'Не верно. Что бы продолжить, нажми "Новый вопрос"'
            )
        return QUESTION


def handle_losing_attempt(
        update: Update, context: CallbackContext, redis_connect, questions_file
):
    question = redis_connect.get(update.effective_chat.id).decode('utf-8')
    with open(questions_file) as questions:
        questions = json.loads(questions.read())
        answer = questions[question]
        update.message.reply_text(
            f'Верный ответ: {answer}. Что бы продолжить, нажми "Новый вопрос"'
        )
    return QUESTION


def main() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    env = Env()
    env.read_env()
    tg_token = env.str('TG_TOKEN')
    questions_file = env.str('PATH_QUESTIONS_FILE', './questions.json')
    redis_host = env.str('REDIS_HOST')
    redis_port = env.str('REDIS_PORT')
    redis_pass = env.str('REDIS_PASS')

    pool = redis.ConnectionPool(
        host=redis_host, port=redis_port, db=0, password=redis_pass
    )
    redis_connect = redis.Redis(connection_pool=pool)

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    quiz_quest_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                Filters.text('Новый вопрос') & ~Filters.command,
                lambda update, context: handle_new_question_request(
                    update, context, redis_connect, questions_file
                )
            )
        ],
        states={
            QUESTION: [
                MessageHandler(
                    Filters.text('Новый вопрос') & ~Filters.command,
                    lambda update, context: handle_new_question_request(
                        update, context, redis_connect, questions_file
                    )
                )
            ],
            CHECK_QUESTION_ANSWER: [
                MessageHandler(
                    Filters.text & ~Filters.text('Сдаться'),
                    lambda update, context: handle_solution_attempt(
                    update, context, redis_connect, questions_file
                    )
                ),
                MessageHandler(
                    Filters.text('Сдаться') & ~Filters.command,
                    lambda update, context: handle_losing_attempt(
                        update, context, redis_connect, questions_file
                    )
                ),
            ],
        },
        fallbacks=[]
    )

    dispatcher.add_handler(quiz_quest_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
