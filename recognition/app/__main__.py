"""
Приложение для распознавания голосовых сообщений.
Тестовое задание x-lab.
"""

import os
import argparse
import logging
import uuid
import datetime

from recognition.db.db import db
from recognition.app.pars_respons import positive_or_negative_answer, answerphone
from recognition.utils.recognize_tools import duration_adaption
from recognition.app.pars_respons import error_logger

parser = argparse.ArgumentParser(description='application parameters')
parser.add_argument('--file', required=True, help='The path to the file .wav')
parser.add_argument('--phone', required=True, help='Phone number')
parser.add_argument('--to-base', choices=['true', 'false'],
                    default='false', help='Add results to base')
parser.add_argument('--stage', required=True, choices=['1', '2'], help='Recognition stage')

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s:%(asctime)s:%(message)s')
file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def main():
    args = parser.parse_args()
    id_ = uuid.uuid4()
    msg = 'id: {0}, result: {1}, phone number: {2}, duration: {3}, transcript: {4}'
    try:
        if args.stage == '1':
            result, transcript, duration = answerphone(args)
        else:
            result, transcript, duration = positive_or_negative_answer(args)
        logger.info(msg.format(id_, result, args.phone, duration, transcript))
        os.remove(args.file)

        # если есть флаг записи в базу.
        if args.to_base == 'true':
            duration = duration_adaption(duration)  # приводим время воспр. к float
            date = datetime.date.today()
            time = datetime.datetime.now().time()
            db.add_to_db(date, time, id_, result, args.phone, duration, transcript)
    except Exception as e:
        error_logger.exception(e)


if __name__ == '__main__':
    main()
