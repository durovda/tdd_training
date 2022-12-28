import pytest

from dialog_with_user import DialogWithUser
from custom_exceptions import PatientIdNotIntegerAndPositiveError
from mock_console import MockConsole
from command_type import CommandType


def test_request_patient_id():
    console = MockConsole()
    console.add_expected_request_and_response('Введите ID пациента: ', '3')
    dialog = DialogWithUser(console)
    assert dialog.request_patient_id() == 3


def test_request_patient_id_when_id_not_integer():
    console = MockConsole()
    console.add_expected_request_and_response('Введите ID пациента: ', 'три')
    dialog = DialogWithUser(console)
    with pytest.raises(PatientIdNotIntegerAndPositiveError) as err:
        dialog.request_patient_id()
    assert str(err.value) == 'Ошибка ввода. ID пациента должно быть числом (целым, положительным)'


def test_request_patient_id_when_id_not_positive():
    console = MockConsole()
    console.add_expected_request_and_response('Введите ID пациента: ', '-2')
    dialog = DialogWithUser(console)
    with pytest.raises(PatientIdNotIntegerAndPositiveError) as err:
        dialog.request_patient_id()
    assert str(err.value) == 'Ошибка ввода. ID пациента должно быть числом (целым, положительным)'


fixture_for_parser = [('стоп', CommandType.STOP),
                      ('Стоп', CommandType.STOP),
                      ('stop', CommandType.STOP),
                      ('STOP', CommandType.STOP),
                      ('остановите программу!', CommandType.UNKNOWN),
                      ('узнать статус пациента', CommandType.GET_STATUS),
                      ('get status', CommandType.GET_STATUS),
                      ('повысить статус пациента', CommandType.STATUS_UP),
                      ('status up', CommandType.STATUS_UP),
                      ('понизить статус пациента', CommandType.STATUS_DOWN),
                      ('status down', CommandType.STATUS_DOWN),
                      ('выписать пациента', CommandType.DISCHARGE),
                      ('discharge', CommandType.DISCHARGE),
                      ('рассчитать статистику', CommandType.CALCULATE_STATISTICS),
                      ('calculate statistics', CommandType.CALCULATE_STATISTICS),
                      ]


@pytest.mark.parametrize('command_as_text, command_type', fixture_for_parser)
def test_parse_text_to_command(command_as_text, command_type):
    dialog = DialogWithUser()
    assert dialog._parse_text_to_command(command_as_text) == command_type


def test_request_command():
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    dialog = DialogWithUser(console)
    assert dialog.request_command() == CommandType.STOP


def test_request_confirmation_of_patient_discharge():
    console = MockConsole()
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет) ', 'да')
    dialog = DialogWithUser(console)
    assert dialog.request_confirmation_of_patient_discharge()


def test_request_not_confirmation_of_patient_discharge():
    console = MockConsole()
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет) ', 'нет')
    dialog = DialogWithUser(console)
    assert not dialog.request_confirmation_of_patient_discharge()


def test_request_not_confirmation_of_patient_discharge_when_invalid_response():
    console = MockConsole()
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет) ', 'не надо')
    dialog = DialogWithUser(console)
    assert not dialog.request_confirmation_of_patient_discharge()


def test_send_message():
    console = MockConsole()
    console.add_expected_output_message('Сообщение, посылаемое пользователю')
    dialog = DialogWithUser(console)
    dialog.send_message('Сообщение, посылаемое пользователю')
