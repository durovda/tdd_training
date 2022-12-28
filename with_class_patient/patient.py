
class Patient:
    _statuses_db = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}

    def __init__(self, patient_id, status_code=1):
        self._patient_id = patient_id
        self._status_code = status_code
        # self._statuses_db = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}

    @staticmethod
    def get_available_status_set():
        return [value for key, value in Patient._statuses_db.items()]

    def get_id(self):
        return self._patient_id

    def get_status(self):
        return self._statuses_db[self._status_code]

    def status_up(self):
        self._status_code += 1

    def status_down(self):
        self._status_code -= 1
