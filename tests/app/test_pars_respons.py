import argparse

from recognition.app.pars_respons import answerphone, positive_or_negative_answer


def test_answerphone_return_not_person():
    args = argparse.Namespace(file='1.wav')
    result = answerphone(args)
    expect = 'АО'
    assert result[0] == expect


def test_answerphone_return_person():
    args = argparse.Namespace(file='2.wav')
    result = answerphone(args)
    expect = 'Человек'
    assert result[0] == expect


def test_positive_answer():
    args = argparse.Namespace(file='2.wav')
    result = positive_or_negative_answer(args)
    expect = 'Положительно'
    assert result[0] == expect


def test_negative_answer():
    args = argparse.Namespace(file='4.wav')
    result = positive_or_negative_answer(args)
    expect = 'Отрицательно'
    assert result[0] == expect
