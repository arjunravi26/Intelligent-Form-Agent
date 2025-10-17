from faker import Faker
import random
import json
import os
import yaml

OUTPUT_DIR = 'data\claim'
CONFIG_PATH = "data_creation/config.yaml"
MIN_CLAIMS_PER_PATIENT = 2
MAX_CLAIMS_PER_PATIENT = 6

fake = Faker()
with open(CONFIG_PATH, "r") as file:
    data = yaml.safe_load(file)

ICD_CODES = data["ICD_CODES"]
CPT_CODES = data["CPT_CODES"]
DRUG_NAMES = data["DRUG_NAMES"]
PROVIDER_NAMES = data["PROVIDER_NAMES"]


def create_patient_profile(patient_id):
    return {
        "patient_id": patient_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "date_of_birth": fake.date_between(start_date="-70y", end_date="-20y").isoformat(),
        "policy_number": fake.bothify(text='P#####-##')
    }


def generate_claim(patient_profile, base_diagnosis, claim_number_offset):
    procedure_key = "Office Visit (Established Patient)"
    provider = random.choice(PROVIDER_NAMES)

    if base_diagnosis == "Hypertension":
        procedure_key = "Echocardiogram"
        provider = PROVIDER_NAMES[2]
    elif base_diagnosis == "Migraine":
        procedure_key = "MRI Brain w/o Contrast"
        provider = PROVIDER_NAMES[1]
    elif base_diagnosis == "Asthma":
        procedure_key = "Spirometry (Lung Function Test)"
        provider = PROVIDER_NAMES[4]
    elif base_diagnosis == "Type 2 Diabetes":
        procedure_key = "Blood Glucose Test"
        provider = PROVIDER_NAMES[0]

    procedure_code = CPT_CODES[procedure_key]

    visit_date = fake.date_between(
        start_date=f"-{claim_number_offset}M", end_date=f"-{claim_number_offset}M").isoformat()

    billed_amount = round(random.uniform(500.0, 3500.0), 2)
    allowed_amount = round(billed_amount * random.uniform(0.65, 0.85), 2)
    copay = random.choice([25.0, 50.0, 75.0])
    insurance_paid = round(allowed_amount - copay, 2)

    summary = (
        f"Claim for {base_diagnosis} ({ICD_CODES[base_diagnosis]}). "
        f"Patient presented with symptoms requiring {procedure_key} ({procedure_code}). "
        f"Recommended medication: {random.choice(DRUG_NAMES)}."
    )

    clinical_note = (
        f"CLINICAL NOTE: Patient {patient_profile['first_name']} {patient_profile['last_name']} (Policy: {patient_profile['policy_number']}) "
        f"was seen today, {visit_date}, by {provider}. The main subjective complaint was a "
        f"recurrent flare-up of their **{base_diagnosis}** symptoms, which are generally well-managed. "
        f"{fake.paragraph(nb_sentences=2)} Assessment determined the necessity of a diagnostic "
        f"procedure to confirm the severity: **{procedure_key}** (CPT: {procedure_code}). "
        f"The diagnosis code assigned is **{ICD_CODES[base_diagnosis]}**. The patient was advised "
        f"on the necessity of lifestyle modifications and will be starting the new medication, "
        f"{random.choice(DRUG_NAMES)}, immediately. Total billed charges for this visit are ${billed_amount:.2f}. "
        f"All staff were informed regarding the high priority of the patient's next appointment."
    )

    structured_details = {
        "claim_id": fake.bothify(text='CLM#########'),
        "claim_date": visit_date,
        "patient_info": patient_profile,
        "provider_name": provider,
        "primary_diagnosis": base_diagnosis,
        "icd_code": ICD_CODES[base_diagnosis],
        "procedure_description": procedure_key,
        "cpt_code": procedure_code,
        "financials": {
            "billed_amount": billed_amount,
            "allowed_amount": allowed_amount,
            "copay": copay,
            "insurance_paid": insurance_paid
        }
    }

    return structured_details, clinical_note, summary



def save_claim_files(structured_details, unstructured_note, summary):

    patient_id = structured_details['patient_info']['patient_id']
    claim_id = structured_details['claim_id']

    claim_dir = os.path.join(OUTPUT_DIR, patient_id, claim_id)

    os.makedirs(claim_dir, exist_ok=True)

    with open(os.path.join(claim_dir, 'claim_details.json'), 'w') as f:
        json.dump(structured_details, f, indent=4)

    text_content = (
        "---CLINICAL NOTE ---\n"
        f"{unstructured_note}\n\n"
        "---SUMMARY ---\n"
        f"{summary}\n"
    )

    with open(os.path.join(claim_dir, 'claim_text_data.txt'), 'w') as f:
        f.write(text_content)


patient_profiles = {
    "PA-12345": create_patient_profile("PA-12345"),
    "PB-24680": create_patient_profile("PB-24680"),
    "PC-13579": create_patient_profile("PC-13579"),
    "PD-09876": create_patient_profile("PD-09876"),
    "PE-54321": create_patient_profile("PE-54321"),
}

patient_conditions = {
    "PA-12345": "Hypertension",
    "PB-24680": "Migraine",
    "PC-13579": "Asthma",
    "PD-09876": "Type 2 Diabetes",
    "PE-54321": "Acute Sinusitis",
}

total_claims_generated = 0
all_icd_keys = list(ICD_CODES.keys())
print("--- STARTING DYNAMIC TEST DATA GENERATION ---")
for patient_id, base_condition in patient_conditions.items():
    patient = patient_profiles[patient_id]

    num_claims = random.randint(MIN_CLAIMS_PER_PATIENT, MAX_CLAIMS_PER_PATIENT)
    print(
        f"Generating {num_claims} claims for Patient {patient_id} ({base_condition})...")

    for i in range(1, num_claims + 1):
        current_diagnosis = base_condition
        if random.random() < 0.25 and len(all_icd_keys) > 1:
            available_diagnoses = [d for d in all_icd_keys if d != base_condition]
            if available_diagnoses:
                current_diagnosis = random.choice(available_diagnoses)
        structured, unstructured, summary = generate_claim(
            patient, current_diagnosis, num_claims - i + 1)
        save_claim_files(structured, unstructured, summary)
        total_claims_generated += 1

print("--- FILE GENERATION COMPLETE ---")
print(f"Total Claims Generated: {total_claims_generated}")
print(f"Data is organized in the '{OUTPUT_DIR}' directory.")
print("\nExample Path Structure (Note the single text file):")
print(f"  {OUTPUT_DIR}/PA-12345/CLM#########/claim_details.json")
print(f"  {OUTPUT_DIR}/PA-12345/CLM#########/claim_text_data.txt")
