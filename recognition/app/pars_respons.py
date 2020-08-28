"""Функции распознаия ответа API"""
import os
from argparse import Namespace

from tinkoff_voicekit_client import ClientSTT
from fuzzywuzzy import process

from recognition.utils.error_log import error_logger


API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

client = ClientSTT(API_KEY, SECRET_KEY)
audio_config = {
    "encoding": "LINEAR16",
    "sample_rate_hertz": 8000,
    "num_channels": 1,
}


def get_data(args: Namespace) -> tuple:
    """
    Функция возвращает кортеж с распознаным текстом аудио файла и
    продолжительность.
    """
    try:
        response = client.recognize(args.file, audio_config)
        transcript = response[0]['alternatives'][0]['transcript']  # распознаный текст
        duration = response[-1]['end_time']  # продрлжительность
        return transcript, duration
    except Exception as e:
        error_logger.exception(e)


def answerphone(args: Namespace) -> tuple:
    """
    Функция распознаёт на аудио заиписи автоотвечик.
    Если автоотвечик, возвращает 0 иначе 1.
    """
    transcript, duration = get_data(args)
    if 'автоответчик' in transcript.split():
        print(0)
        return 'АО', transcript, duration  # сразу возвращаем текст и продолжительность
    else:                                  # чтобы не делать лишних запросов к API.
        print(1)
        return 'Человек', transcript, duration


def positive_or_negative_answer(args: Namespace) -> tuple:
    """
    Функция распознаёт на аудио заиписи положительный или отрицательный
    ответ человека. Если положительный, возвращает 1 иначе 0.
    """
    transcript, duration = get_data(args)

    # ключевые слова для положительных и отрицательных ответов
    positive_key_words = ['удобно', 'говорите', 'конечно', 'слушаю']
    negative_key_words = ['нет', 'занят', 'неудобно', 'отвлекаете', 'на работе']

    # получаем процент совпадения текста с ключевыми словами
    _, positive = process.extractOne(transcript, positive_key_words)
    _, negative = process.extractOne(transcript, negative_key_words)

    if positive > negative:
        print(1)
        return 'Положительно', transcript, duration
    else:
        print(0)
        return 'Отрицательно', transcript, duration
