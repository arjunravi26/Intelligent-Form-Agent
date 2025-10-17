from faker import Faker
import random
import json

# Initialize Faker
fake = Faker()

# --- Domain-Specific Data Lists for Realism ---
# ICD-10 Diagnosis Codes (Common conditions)
ICD_CODES = {
    "Hypertension": "I10",
    "Type 2 Diabetes": "E11.9",
    "Migraine": "G43.909",
    "Asthma": "J45.909",
    "Acute Sinusitis": "J01.90"
}

# CPT Procedure Codes (Common services)
CPT_CODES = {
    "Office Visit (Established Patient)": "99214",
    "Office Visit (New Patient)": "99203",
    "MRI Brain w/o Contrast": "70551",
    "Blood Glucose Test": "82947",
    "Echocardiogram": "93306",
    "Spirometry (Lung Function Test)": "94010"
}

DRUG_NAMES = [
    "Lisinopril (20mg)", "Metformin (500mg)", "Atorvastatin (10mg)",
    "Sumatriptan (100mg)", "Albuterol HFA", "Amoxicillin (500mg)", "Fluticasone Propionate"
]

PROVIDER_NAMES = [
    "Dr. Eleanor Vance (Internal Medicine)", "Dr. Marcus Bell (Neurology)",
    "Dr. Ava Sharma (Cardiology)", "Central City Hospital", "Dr. David Chen (Pulmonology)"
]

def create_patient_profile(patient_id):
    """Creates a consistent patient profile for all related claims."""
    return {
        "patient_id": patient_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "date_of_birth": fake.date_between(start_date="-70y", end_date="-20y").isoformat(),
        "policy_number": fake.bothify(text='P#####-##')
    }

def generate_claim(patient_profile, base_diagnosis, claim_number_offset):
    """Generates a single claim dictionary based on a patient profile."""

    # Select procedure and provider based on the diagnosis
    procedure_key = "Office Visit (Established Patient)"
    provider = random.choice(PROVIDER_NAMES)

    if base_diagnosis == "Hypertension":
        procedure_key = "Echocardiogram"
        provider = PROVIDER_NAMES[2] # Cardiology
    elif base_diagnosis == "Migraine":
        procedure_key = "MRI Brain w/o Contrast"
        provider = PROVIDER_NAMES[1] # Neurology
    elif base_diagnosis == "Asthma":
        procedure_key = "Spirometry (Lung Function Test)"
        provider = PROVIDER_NAMES[4] # Pulmonology
    elif base_diagnosis == "Type 2 Diabetes":
        procedure_key = "Blood Glucose Test"
        provider = PROVIDER_NAMES[0] # Internal Medicine

    procedure_code = CPT_CODES[procedure_key]

    # Set dates sequentially for multi-form analysis (tracking treatment)
    visit_date = fake.date_between(start_date=f"-{claim_number_offset}M", end_date=f"-{claim_number_offset}M").isoformat()

    # Generate mock cost data
    billed_amount = round(random.uniform(500.0, 3500.0), 2)
    allowed_amount = round(billed_amount * random.uniform(0.65, 0.85), 2)
    copay = random.choice([25.0, 50.0, 75.0])
    insurance_paid = round(allowed_amount - copay, 2)

    # Generate a relevant summary/plan
    summary = (
        f"Claim for {base_diagnosis} ({ICD_CODES[base_diagnosis]}). "
        f"Patient presented with symptoms requiring {procedure_key} ({procedure_code}). "
        f"Recommended medication: {random.choice(DRUG_NAMES)}."
    )

    # --- NEW: Generate Unstructured Data (Doctor's Note Simulation) ---
    unstructured_note = (
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

    return {
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
        },
        "extracted_summary": summary,
        "note": unstructured_note,
    }

# --- Data Generation Logic ---

# 1. Create five distinct patients
patient_A = create_patient_profile("PA-12345") # 5 claims: Chronic Hypertension
patient_B = create_patient_profile("PB-24680") # 3 claims: Mixed issues
patient_C = create_patient_profile("PC-13579") # 3 claims: Chronic Asthma
patient_D = create_patient_profile("PD-09876") # 2 claims: Acute issues
patient_E = create_patient_profile("PE-54321") # 2 claims: Chronic Type 2 Diabetes

all_claims = []

# 2. Generate 5 claims for Patient A (Chronic condition tracking - Hypertension)
for i in range(5):
    all_claims.append(generate_claim(patient_A, "Hypertension", 5 - i))

# 3. Generate 3 claims for Patient B (Acute and chronic issues)
all_claims.append(generate_claim(patient_B, "Migraine", 3))
all_claims.append(generate_claim(patient_B, "Acute Sinusitis", 2))
all_claims.append(generate_claim(patient_B, "Type 2 Diabetes", 1))

# 4. Generate 3 claims for Patient C (Chronic condition tracking - Asthma)
for i in range(3):
    all_claims.append(generate_claim(patient_C, "Asthma", 3 - i))

# 5. Generate 2 claims for Patient D (Acute issues)
all_claims.append(generate_claim(patient_D, "Acute Sinusitis", 4))
all_claims.append(generate_claim(patient_D, "Migraine", 1))

# 6. Generate 2 claims for Patient E (Chronic condition tracking - Type 2 Diabetes)
for i in range(2):
    all_claims.append(generate_claim(patient_E, "Type 2 Diabetes", 2 - i))


# Final Output
print("--- TEST DATA GENERATION COMPLETE ---")
print(f"Total Claims Generated: {len(all_claims)}")
print("\nSample Output (First Claim):\n")
print(json.dumps(all_claims[0], indent=2))
print("\n--- Saving All Claims to JSON File ---")

# Save the data to a JSON file (the standard format for test data)
output_filepath = 'data/mock_medical_claims.json'
try:
    with open(output_filepath, 'w') as f:
        json.dump(all_claims, f, indent=2)
    print(f"Data saved successfully to {output_filepath}")
except FileNotFoundError:
    print(f"Warning: Could not save to '{output_filepath}'. Ensure the 'data' directory exists.")
except Exception as e:
    print(f"An error occurred while saving the file: {e}")
