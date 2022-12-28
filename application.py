from command_type import CommandType


class Application:
    def __init__(self, dialog_with_user=None, commands=None):
        self._dialog_with_user = dialog_with_user
        self._commands = commands

    def main(self):
        stop = False
        while not stop:
            command_type = self._dialog_with_user.request_command()
            if command_type == CommandType.GET_STATUS:
                self._commands.get_status()
            elif command_type == CommandType.STATUS_UP:
                self._commands.status_up()
            elif command_type == CommandType.STATUS_DOWN:
                self._commands.status_down()
            elif command_type == CommandType.DISCHARGE:
                self._commands.discharge()
            elif command_type == CommandType.CALCULATE_STATISTICS:
                self._commands.calculate_statistics()
            elif command_type == CommandType.STOP:
                self._dialog_with_user.send_message('Сеанс завершён.')
                stop = True
            elif command_type == CommandType.UNKNOWN:
                self._dialog_with_user.send_message('Неизвестная команда! Попробуйте ещё раз')
