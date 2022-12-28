from unittest.mock import MagicMock

from hospital_commands import Commands
from custom_exceptions import PatientIdNotIntegerAndPositiveError, PatientNotExistsError, MinStatusCannotDownError


def test_get_status():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.get_patient_status_by_id = MagicMock(return_value='Слегка болен')
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.get_status()

    cmd._dialog_with_user.send_message.assert_called_with('Статус пациента: "Слегка болен"')


def test_get_status_when_patient_id_not_integer():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(side_effect=PatientIdNotIntegerAndPositiveError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.get_status()

    cmd._dialog_with_user.send_message.assert_called_with('Ошибка ввода. '
                                                          'ID пациента должно быть числом (целым, положительным)')


def test_get_status_when_patient_not_exists():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=999)
    cmd._hospital.get_patient_status_by_id = MagicMock(side_effect=PatientNotExistsError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.get_status()

    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_status_up():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.can_patient_status_up = MagicMock(return_value=True)
    cmd._hospital.patient_status_up = MagicMock()
    cmd._hospital.get_patient_status_by_id = MagicMock(return_value='Готов к выписке')
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._hospital.patient_status_up.assert_called_with(77)
    cmd._dialog_with_user.send_message.assert_called_with('Новый статус пациента: "Готов к выписке"')


def test_status_up_when_patient_id_not_integer():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(side_effect=PatientIdNotIntegerAndPositiveError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.send_message.assert_called_with('Ошибка ввода. '
                                                          'ID пациента должно быть числом (целым, положительным)')


def test_status_up_when_patient_not_exists():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=999)
    cmd._hospital.can_patient_status_up = MagicMock(side_effect=PatientNotExistsError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_status_up_when_patient_discharge():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.can_patient_status_up = MagicMock(return_value=False)
    cmd._dialog_with_user.request_confirmation_of_patient_discharge = MagicMock(return_value=True)
    cmd._hospital.patient_discharge = MagicMock()
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._hospital.patient_discharge.assert_called_with(77)
    cmd._dialog_with_user.send_message.assert_called_with('Пациент выписан из больницы')


def test_status_up_when_status_not_changed():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.can_patient_status_up = MagicMock(return_value=False)
    cmd._dialog_with_user.request_confirmation_of_patient_discharge = MagicMock(return_value=False)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.send_message.assert_called_with('Пациент остался в статусе "Готов к выписке"')


def test_status_down():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.patient_status_down = MagicMock()
    cmd._hospital.get_patient_status_by_id = MagicMock(return_value='Слегка болен')
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_down()

    cmd._hospital.patient_status_down.assert_called_with(77)
    cmd._dialog_with_user.send_message.assert_called_with('Новый статус пациента: "Слегка болен"')


def test_status_down_when_patient_id_not_integer():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(side_effect=PatientIdNotIntegerAndPositiveError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_down()

    cmd._dialog_with_user.send_message.assert_called_with('Ошибка ввода. '
                                                          'ID пациента должно быть числом (целым, положительным)')


def test_status_down_when_patient_not_exists():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=999)
    cmd._hospital.patient_status_down = MagicMock(side_effect=PatientNotExistsError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_down()

    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_status_down_when_min_status_cannot_down():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.patient_status_down = MagicMock(side_effect=MinStatusCannotDownError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_down()

    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. Нельзя понизить самый низкий статус '
                                                          '(наши пациенты не умирают)')


def test_discharge():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.patient_discharge = MagicMock()
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.discharge()

    cmd._hospital.patient_discharge.assert_called_with(77)
    cmd._dialog_with_user.send_message.assert_called_with('Пациент выписан из больницы')


def test_discharge_when_patient_id_not_integer():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(side_effect=PatientIdNotIntegerAndPositiveError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.discharge()

    cmd._dialog_with_user.send_message.assert_called_with('Ошибка ввода. '
                                                          'ID пациента должно быть числом (целым, положительным)')


def test_discharge_when_patient_not_exists():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=999)
    cmd._hospital.patient_discharge = MagicMock(side_effect=PatientNotExistsError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.discharge()

    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_calculate_statistics():
    cmd = Commands(hospital=MagicMock(), dialog_with_user=MagicMock())
    cmd._hospital.get_statistics = MagicMock(return_value={"Тяжело болен": 1, "Болен": 3, "Готов к выписке": 2})
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.calculate_statistics()

    cmd._dialog_with_user.send_message.assert_called_with('Статистика по статусам:\n'
                                                          ' - в статусе "Тяжело болен": 1 чел.\n'
                                                          ' - в статусе "Болен": 3 чел.\n'
                                                          ' - в статусе "Готов к выписке": 2 чел.')
