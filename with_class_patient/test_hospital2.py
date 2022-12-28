import pytest

from custom_exceptions import PatientNotExistsError
from with_class_patient.hospital_2 import Hospital
from with_class_patient.patient import Patient


def status_code_list_to_patients_db(status_code_list):
    patients_db = []
    patient_id = 1
    for status_code in status_code_list:
        patients_db.append(Patient(patient_id, status_code))
        patient_id += 1
    return patients_db


def test_get_patients_db_as_status_code_list():
    patients_db = [Patient(1, status_code=0),
                   Patient(2, status_code=3)]
    hospital = Hospital(patients_db)
    assert hospital.get_patients_db_as_status_code_list() == [0, 3]


def test_get_patient_status_by_id():
    patients_db = [Patient(1, status_code=0),
                   Patient(2, status_code=3),
                   Patient(3, status_code=0)]
    hospital = Hospital(patients_db)
    assert hospital.get_patient_status_by_id(2) == "Готов к выписке"


def test_patient_not_exists_error():
    hospital = Hospital([Patient(1, status_code=1)])
    with pytest.raises(PatientNotExistsError) as err:
        hospital.get_patient_status_by_id(99)
    assert str(err.value) == 'Ошибка. В больнице нет пациента с таким ID'


def test_patient_status_up():
    hospital = Hospital([Patient(1, status_code=1)])
    hospital.patient_status_up(1)
    assert hospital.get_patient_status_by_id(1) == "Слегка болен"


def test_get_statistics():
    patients_db = status_code_list_to_patients_db([2, 1, 1, 1, 2])
    hospital = Hospital(patients_db)
    statistics = hospital.get_statistics()
    assert statistics == {"Болен": 3, "Слегка болен": 2}
