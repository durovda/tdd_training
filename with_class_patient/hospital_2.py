from custom_exceptions import PatientNotExistsError
from with_class_patient.patient import Patient


class Hospital:
    def __init__(self, patients_db):
        self._patients_db = patients_db

    def _get_patient_by_id(self, patient_id):
        for patient in self._patients_db:
            if patient.get_id() == patient_id:
                return patient
        raise PatientNotExistsError()

    def get_patient_status_by_id(self, patient_id):
        patient = self._get_patient_by_id(patient_id)
        return patient.get_status()

    def patient_status_up(self, patient_id):
        patient = self._get_patient_by_id(patient_id)
        patient.status_up()

    def get_patients_db_as_status_code_list(self):
        status_code_list = []
        for patient in self._patients_db:
            status_code_list.append(patient._status_code)
        return status_code_list

    def get_statistics(self):
        statuses_set = Patient.get_available_status_set()
        statistics = {}
        for status in statuses_set:
            count = 0
            for patient in self._patients_db:
                if patient.get_status() == status:
                    count += 1
            if count > 0:
                statistics[status] = count
        return statistics
