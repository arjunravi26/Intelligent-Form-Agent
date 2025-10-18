from src.config import read_config
from huggingface_hub import InferenceClient
import os
import json


class AbstractiveQA:
    def __init__(self):
        self.system_prompt = read_config('SYSTEM_PROMPT_ABSTRACIVE_QA')
        if not self.system_prompt:
            raise "No System prompt available."
        self.model = read_config("LLM_MODEL")

    def qa(self, data: str, question: str):
        try:

            user_query = (
                f"Based on the following clinical note, please answer my question.\n\n"
                f"--- CLAIM DETAILS ---\n"
                f"{data}\n\n"
                f"--- QUESTION ---\n"
                f"{question}"
            )
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_query}
            ]
            client = InferenceClient(token=os.getenv("HF_TOKEN"))

            response = client.chat_completion(
                messages=messages,
                model=self.model,
                max_tokens=512,
                temperature=0.1,

            )
            result = response.choices[0].message.content
            json_result = json.loads(result)
            return json_result['answer'], json_result['reasoning']
        except Exception as e:
            print(f"Raise Exception {e}")
            return None


if __name__ == "__main__":
    from src.data_ingestion import DataIngestion
    data_ingestion = DataIngestion(patient_id="PA-12345")
    claim_data = data_ingestion.ingest_claim_data(claim_path='CLM153910000')
    abstractive_qa = AbstractiveQA()
    result = abstractive_qa.qa(data=claim_data, question="Who is the doctor")
    print(result)
