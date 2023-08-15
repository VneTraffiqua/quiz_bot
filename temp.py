# -*- coding: utf-8 -*-
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from environs import Env


def main():
    """ Пример создания клавиатуры для отправки ботом """
    env = Env()
    env.read_env()
    api = env.str('VK_TOKEN')
    vk_session = vk_api.VkApi(token=api)
    vk = vk_session.get_api()

    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Белая кнопка', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)

    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_button('Красная кнопка', color=VkKeyboardColor.NEGATIVE)

    keyboard.add_line()
    keyboard.add_button('Синяя кнопка', color=VkKeyboardColor.PRIMARY)

    vk.messages.send(
        peer_id=123456,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='Пример клавиатуры'
    )