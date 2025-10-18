from src.config import read_config
from huggingface_hub import InferenceClient
from src.utils.utils import process_data
from dotenv import load_dotenv
import os



class ExtractiveQA:
    def __init__(self, claim_data: str):
        if isinstance(claim_data, dict):
            self.claim_data = process_data(data=claim_data)
        else:
            self.claim_data = claim_data
        self.model_name = read_config('EXTRACTIVE_QA_MODEL_NAME')


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
