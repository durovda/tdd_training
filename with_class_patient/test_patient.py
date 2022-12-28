from with_class_patient.patient import Patient


def test_create_patient():
    patient = Patient(1, status_code=2)
    assert patient.get_id() == 1
    assert patient.get_status() == "Слегка болен"


def test_create_patient_with_default_status():
    patient = Patient(1)
    assert patient.get_status() == "Болен"


def test_status_up():
    patient = Patient(1, status_code=2)
    patient.status_up()
    assert patient.get_status() == "Готов к выписке"


def test_status_down():
    patient = Patient(1, status_code=2)
    patient.status_down()
    assert patient.get_status() == "Болен"


def test_get_available_status_set():
    expected_status_set = ["Тяжело болен", "Болен", "Слегка болен", "Готов к выписке"]
    assert Patient.get_available_status_set() == expected_status_set
