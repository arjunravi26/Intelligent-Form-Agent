from faker import Faker
from typing import List, Dict
import pandas as pd
import random
import os

fake = Faker()

DIAGNOSES: List[str] = [
    "Hypertension", "Diabetes", "Asthma", "Coronary Artery Disease",
    "Migraine", "COPD", "Hypothyroidism", "Depression", "Anxiety"
]

MEDICATIONS: List[str] = [
    "Metformin", "Lisinopril", "Albuterol", "Aspirin",
    "Levothyroxine", "Atorvastatin", "Omeprazole", "Sertraline", "Fluoxetine"
]

DOCTORS: List[str] = [
    "Dr. Smith", "Dr. Johnson", "Dr. Lee", "Dr. Brown", "Dr. Davis",
    "Dr. Miller", "Dr. Wilson", "Dr. Taylor"
]

VISIT_NOTES_TEMPLATES: List[str] = [
    "Patient presents with {diagnosis}. Recommended {medication} and advised follow-up in {followup_days} days.",
    "During the visit, patient reported symptoms consistent with {diagnosis}. Prescribed {medication}.",
    "Clinical evaluation shows {diagnosis}. Medication {medication} initiated. Monitor response over next {followup_days} days."
]

BASE_DIR: str = "data/samples/medical_records"
os.makedirs(BASE_DIR, exist_ok=True)


def create_patient_record() -> Dict[str, str]:
    patient_id = fake.uuid4()
    name = fake.name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
    gender = random.choice(["Male", "Female", "Other"])
    diagnosis = random.choice(DIAGNOSES)
    medication = random.choice(MEDICATIONS)
    doctor = random.choice(DOCTORS)
    visit_date = fake.date_this_year()
    insurance_id = fake.bothify(text="INS####-####")
    followup_days = random.randint(7, 90)
    visit_notes = random.choice(VISIT_NOTES_TEMPLATES).format(
        diagnosis=diagnosis, medication=medication, followup_days=followup_days
    )

    return {
        "Patient ID": patient_id,
        "Name": name,
        "DOB": dob,
        "Gender": gender,
        "Diagnosis": diagnosis,
        "Medication": medication,
        "Doctor": doctor,
        "Visit Date": visit_date,
        "Insurance ID": insurance_id,
        "Follow-up Days": followup_days,
        "Visit Notes": visit_notes
    }


def save_patient_to_txt(patient: Dict[str, str], directory: str = BASE_DIR) -> None:
    safe_name = patient["Name"].replace(" ", "_")
    file_path = os.path.join(directory, f"{safe_name}.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        for key, value in patient.items():
            f.write(f"{key}: {value}\n")



def generate_patients(no_of_patients: int = 25) -> pd.DataFrame:
    patients = [create_patient_record() for _ in range(no_of_patients)]

    for patient in patients:
        save_patient_to_txt(patient=patient)




if __name__ == "__main__":
    generate_patients(25)
