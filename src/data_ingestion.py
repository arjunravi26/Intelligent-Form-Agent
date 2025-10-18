from src.config import read_config
import os
import json

class DataIngestion:
    "Class to create data ingestion from given patient id"

    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.base_dir = read_config('DATA_PATH')
        self.patient_dir = os.path.join(self.base_dir, self.patient_id)

    def ingest_claim_data(self, claim_path: str):
        "Ingest provided claim data files"
        try:

            if not claim_path:
                return None
            full_claim_path = os.path.join(self.patient_dir, claim_path)
            files = os.listdir(full_claim_path)

            # Extract json path
            details_file = [file for file in files if '.json' in file][0]
            # Full path for josn file, combined with parent dir(claim folder)
            details_file_path = os.path.join(full_claim_path,details_file)
            # Extract txt file
            clinical_note_file = [file for file in files if '.txt' in file][0]
            # Full path for txt file combined with claim folder
            clinical_note_file_path = os.path.join(full_claim_path,clinical_note_file)

            with open(details_file_path, 'r') as file:
                details = json.load(file)

            with open(clinical_note_file_path, 'r') as file:
                clinical_note = file.read()

            details['Clinical_note'] = clinical_note

            return details

        except Exception as e:
            print(e)
            return None

    def ingest_patient_data(self):
        "Ingest all claim data from patient"
        try:
            claim_details = []
            claim_folders = os.listdir(self.patient_dir)
            for claim in claim_folders:
                claim_dif_path = os.path.join(self.patient_dir, claim)
                files = os.listdir(claim_dif_path)
                details_file = [file for file in files if '.json' in file][0]
                details_file_path = os.path.join(claim_dif_path,details_file)
                clinical_note_file = [file for file in files if '.txt' in file][0]
                clinical_note_file_path = os.path.join(claim_dif_path,clinical_note_file)
                with open(details_file_path, 'r') as file:
                    details = json.load(file)
                with open(clinical_note_file_path, 'r') as file:
                    clinical_note = file.read()
                details['Clinical_note'] = clinical_note
                claim_details.append(details)
            return claim_details

        except Exception as e:
            print(e)
            return None


if __name__ == "__main__":
    data_ingestion = DataIngestion(patient_id="PA-12345")
    print(f"Data Ingestion for single claim file(CLM153910000): {data_ingestion.ingest_claim_data(claim_path='CLM153910000')}")
    print(f"Data Ingestion for all claim files: {data_ingestion.ingest_patient_data()}")