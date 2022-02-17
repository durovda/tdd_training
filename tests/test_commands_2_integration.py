from unittest.mock import MagicMock

from commands import Commands
from exceptions import PatientIdNotIntegerError, MinStatusCannotDownError, PatientNotExistsError
from hospital import Hospital
from spesial_asserts import assert_lists_equal


def raise_id_not_integer_error():
    raise PatientIdNotIntegerError


def raise_patient_not_exists_error():
    raise PatientNotExistsError


def raise_min_status_cannot_down_error():
    raise MinStatusCannotDownError


class MockDialogWithUser:
    pass


def test_stop():
    cmd = Commands(dialog_with_user=MagicMock())
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.stop()

    cmd._dialog_with_user.send_message.assert_called_with('Сеанс завершён.')


def test_get_status():
    cmd = Commands(Hospital([1, 1, 2]), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=3)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.get_status()

    cmd._dialog_with_user.send_message.assert_called_with('Статус пациента: "Слегка болен"')


def test_get_status_when_patient_id_not_integer():
    cmd = Commands(None, MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = MagicMock(side_effect=PatientIdNotIntegerError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.get_status()

    cmd._dialog_with_user.send_message.assert_called_with('Ошибка ввода. ID пациента должно быть числом '
                                                          '(целым, положительным)')


def test_get_status_when_patient_not_exists():
    cmd = Commands(Hospital([1]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=999)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.get_status()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_status_up():
    cmd = Commands(Hospital([1, 1, 1, 2]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=4)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Новый статус пациента: "Готов к выписке"')
    assert_lists_equal(cmd._hospital._patients_db, [1, 1, 1, 3])


def test_status_up_when_patient_id_not_integer():
    cmd = Commands(None, MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = MagicMock(side_effect=PatientIdNotIntegerError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка ввода. '
                                                          'ID пациента должно быть числом (целым, положительным)')


def test_status_up_when_patient_not_exists():
    cmd = Commands(Hospital([1]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=999)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_status_up_when_patient_discharge():
    cmd = Commands(Hospital([1, 1, 1, 3]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=4)
    cmd._dialog_with_user.request_patient_discharge_confirmation = MagicMock(return_value=True)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.request_patient_discharge_confirmation.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Пациент выписан из больницы')
    assert_lists_equal(cmd._hospital._patients_db, [1, 1, 1])


def test_status_up_when_status_not_changed():
    cmd = Commands(Hospital([1, 1, 1, 3]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=4)
    cmd._dialog_with_user.request_patient_discharge_confirmation = MagicMock(return_value=False)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.request_patient_discharge_confirmation.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Пациент остался в статусе "Готов к выписке"')
    assert_lists_equal(cmd._hospital._patients_db, [1, 1, 1, 3])


def test_status_down():
    cmd = Commands(Hospital([1, 1, 1, 3]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=4)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_down()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Новый статус пациента: "Слегка болен"')
    assert_lists_equal(cmd._hospital._patients_db, [1, 1, 1, 2])


def test_status_down_when_patient_id_not_integer():
    cmd = Commands(None, MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = MagicMock(side_effect=PatientIdNotIntegerError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_down()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка ввода. '
                                                          'ID пациента должно быть числом (целым, положительным)')


def test_status_down_when_patient_not_exists():
    cmd = Commands(Hospital([1]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=999)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_down()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_status_down_when_min_status_cannot_down():
    cmd = Commands(Hospital([1, 0]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=2)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_down()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. Нельзя понизить самый низкий статус '
                                                          '(наши пациенты не умирают)')


def test_calculate_statistics():
    cmd = Commands(Hospital([1, 3, 1, 0, 1, 3]), MockDialogWithUser())
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.calculate_statistics()

    cmd._dialog_with_user.send_message.assert_called_with('Статистика по статусам:\n'
                                                          ' - в статусе "Тяжело болен": 1 чел.\n'
                                                          ' - в статусе "Болен": 3 чел.\n'
                                                          ' - в статусе "Готов к выписке": 2 чел.')


# def test_discharge_patient():
#     pass
