import pytest

from mock_console import MockConsole


def test_input():
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '7')

    assert console.input('Введите команду: ') == 'узнать статус пациента'
    assert console.input('Введите ID пациента: ') == '7'


def test_input_when_invalid_request():
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'для этого теста подходит любой ответ')

    with pytest.raises(AssertionError):
        console.input('Пожалуйста, введите команду: ')


def test_print():
    console = MockConsole()
    console.add_expected_output_message('Статус пациента: "Болен"')
    console.add_expected_output_message('Новый статус пациента: "Слегка болен"')

    console.print('Статус пациента: "Болен"')
    console.print('Новый статус пациента: "Слегка болен"')


def test_print_when_invalid_output_message():
    console = MockConsole()
    console.add_expected_output_message('Статус пациента: "Болен"')

    with pytest.raises(AssertionError):
        console.print('Статус пациента: "Тяжело болен"')


def test_print_when_invalid_order_of_output_message():
    console = MockConsole()
    console.add_expected_output_message('Первое сообщение')
    console.add_expected_output_message('Второе сообщение')

    with pytest.raises(AssertionError):
        console.print('Второе сообщение')


def test_print_when_list_of_expected_messages_is_empty():
    console = MockConsole()
    console.add_expected_output_message('Сообщение')

    console.print('Сообщение')

    with pytest.raises(AssertionError):
        console.print('Второе сообщение')


def test_not_verify_all_calls_have_been_made():
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '7')

    console.input('Введите команду: ')

    with pytest.raises(AssertionError):
        console.verify_all_calls_have_been_made()


def test_not_verify_all_calls_have_been_made_2():
    console = MockConsole()
    console.add_expected_output_message('Первое сообщение')
    console.add_expected_output_message('Второе сообщение')

    console.print('Первое сообщение')

    with pytest.raises(AssertionError):
        console.verify_all_calls_have_been_made()