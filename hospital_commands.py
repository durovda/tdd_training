from custom_exceptions import PatientIdNotIntegerAndPositiveError, PatientNotExistsError, \
    MinStatusCannotDownError


class Commands:
    def __init__(self, hospital, dialog_with_user):
        self._hospital = hospital
        self._dialog_with_user = dialog_with_user

    def get_status(self):
        try:
            patient_id = self._dialog_with_user.request_patient_id()
            patient_status = self._hospital.get_patient_status_by_id(patient_id)
            self._dialog_with_user.send_message(f'Статус пациента: "{patient_status}"')
        except (PatientIdNotIntegerAndPositiveError, PatientNotExistsError) as err:
            self._dialog_with_user.send_message(str(err))

    def status_up(self):
        try:
            patient_id = self._dialog_with_user.request_patient_id()
            if self._hospital.can_patient_status_up(patient_id):
                self._hospital.patient_status_up(patient_id)
                new_status = self._hospital.get_patient_status_by_id(patient_id)
                self._dialog_with_user.send_message(f'Новый статус пациента: "{new_status}"')
            else:
                confirmation_of_discharge = self._dialog_with_user.request_confirmation_of_patient_discharge()
                if confirmation_of_discharge:
                    self._hospital.patient_discharge(patient_id)
                    self._dialog_with_user.send_message('Пациент выписан из больницы')
                else:
                    self._dialog_with_user.send_message('Пациент остался в статусе "Готов к выписке"')
        except (PatientIdNotIntegerAndPositiveError, PatientNotExistsError) as err:
            self._dialog_with_user.send_message(str(err))

    def status_down(self):
        try:
            patient_id = self._dialog_with_user.request_patient_id()
            self._hospital.patient_status_down(patient_id)
            new_status = self._hospital.get_patient_status_by_id(patient_id)
            self._dialog_with_user.send_message(f'Новый статус пациента: "{new_status}"')
        except (PatientIdNotIntegerAndPositiveError, PatientNotExistsError, MinStatusCannotDownError) as err:
            self._dialog_with_user.send_message(str(err))

    def calculate_statistics(self):
        result_message = ['Статистика по статусам:']
        statistics = self._hospital.get_statistics()
        for status in statistics:
            result_message.append(f' - в статусе "{status}": {statistics[status]} чел.')
        self._dialog_with_user.send_message('\n'.join(result_message))

    def discharge(self):
        try:
            patient_id = self._dialog_with_user.request_patient_id()
            self._hospital.patient_discharge(patient_id)
            self._dialog_with_user.send_message('Пациент выписан из больницы')
        except (PatientIdNotIntegerAndPositiveError, PatientNotExistsError) as err:
            self._dialog_with_user.send_message(str(err))
