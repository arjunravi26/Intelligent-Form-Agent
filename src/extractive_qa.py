from src.config import read_config
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv


class ExtractiveQA:
    def __init__(self, claim_data: str):
        self.claim_data = claim_data if isinstance(
            claim_data, str) else str(claim_data)
        if isinstance(self.claim_data, dict):
            self.claim_data = self._process_data()
        self.model_name = read_config('EXTRACTIVE_QA_MODEL_NAME')

    def _process_data(self):
        details_str = "\n".join(
            f"{key}: {value}" for key, value in self.claim_data.items() if key != "Clinical_note")
        context = f"{details_str}\nClinical Note:\n{self.claim_data.get('Clinical_note', '')}"
        return context

    def qa(self, question: str):
        try:
            if not self.claim_data or not question:
                return None
            load_dotenv()
            client = InferenceClient(
                provider="hf-inference",
                api_key=os.getenv('HF_TOKEN'),
            )
            answer = client.question_answering(
                question=question,
                context=self.claim_data,
                model=self.model_name,
            )
            return answer
        except Exception as e:
            print(f"Exception: {e}")
            return None


if __name__ == "__main__":
    from src.data_ingestion import DataIngestion
    data_ingestion = DataIngestion(patient_id="PA-12345")
    claim_data = data_ingestion.ingest_claim_data(claim_path='CLM153910000')
    extractive_qa = ExtractiveQA(claim_data=claim_data)
    print(extractive_qa.qa("Who is the doctor?"))
