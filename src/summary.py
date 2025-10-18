from src.config import read_config
from src.utils.utils import process_data
from huggingface_hub import InferenceClient
import os


class Summarization:

    def __init__(self):
        self.summarization_model = read_config("SUMMARIZATION_MODEL")
        if not self.summarization_model:
            raise "Summarization model is not loaded properly."

    def summarize(self, claim_data):
        try:
            if isinstance(claim_data, dict):
                self.claim_data = process_data(data=claim_data)
            else:
                self.claim_data = claim_data

            client = InferenceClient(
                provider="hf-inference",
                api_key=os.getenv('HF_TOKEN'),
            )

            result = client.summarization(
                text=self.claim_data,
                model=self.summarization_model,
            )

            return result
        except Exception as e:
            print(f"Raise Exception {e}")
            return None


if __name__ == "__main__":
    from src.data_ingestion import DataIngestion
    data_ingestion = DataIngestion(patient_id="PA-12345")
    claim_data = data_ingestion.ingest_claim_data(claim_path='CLM153910000')
    summarization = Summarization()
    print(f"Summarization is: {summarization.summarize(claim_data=claim_data)}")
