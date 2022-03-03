from command_type import CommandType
from exceptions import PatientIdNotIntegerError


class DialogWithUser:
    def __init__(self, console=None):
        self._console = console

    def send_message(self, text_message):
        self._console.print(text_message)

    def request_command(self):
        command_as_text = self._console.input('Введите команду: ')
        return self._parse_text_to_command(command_as_text)

    @staticmethod
    def _parse_text_to_command(command_as_text):
        command_as_text = command_as_text.lower()
        mapping_phrases_to_command_type = [
            (['стоп', 'stop'], CommandType.STOP),
            (['узнать статус пациента', 'get status'], CommandType.GET_STATUS),
            (['повысить статус пациента', 'status up'], CommandType.STATUS_UP),
            (['понизить статус пациента', 'status down'], CommandType.STATUS_DOWN),
            (['рассчитать статистику', 'calculate statistics'], CommandType.CALCULATE_STATISTICS)
        ]
        for phrases, command_type in mapping_phrases_to_command_type:
            if command_as_text in phrases:
                return command_type
        return CommandType.UNKNOWN

    def request_patient_id(self):
        try:
            id_as_text = self._console.input('Введите ID пациента: ')
            return int(id_as_text)
        except ValueError:
            raise PatientIdNotIntegerError

    def request_patient_discharge_confirmation(self):
        confirmation_text = self._console.input('Желаете этого клиента выписать? (да/нет) ')
        return confirmation_text in ['да', 'yes']
