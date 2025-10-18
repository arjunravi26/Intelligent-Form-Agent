from src.data_ingestion import DataIngestion
from src.abstractive_qa import AbstractiveQA
from src.extractive_qa import ExtractiveQA
from src.summary import Summarization
from src.holistic_analysis import HolisticAnalysis


class Pipeline:
    def __init__(self,patient_id:str,claim_id:str=None):
        data_ingestoin = DataIngestion(patient_id=patient_id)
        if claim_id:
            self.claim_data = data_ingestoin.ingest_claim_data(claim_path=claim_id)
        else:
            self.claim_data = None
        self.patient_data = data_ingestoin.ingest_patient_data()

    def pipeline(self, option: str, question: str = ""):
        if option == "qa":
            extractive_qa = ExtractiveQA(claim_data=self.claim_data)
            if question:
                return extractive_qa.qa(question=question)
            else:
                return "No question received."

        elif option == "advanced_qa":
            abstractive_qa = AbstractiveQA(claim_data=self.claim_data)
            if question:
                return abstractive_qa.qa(question=question)
            else:
                return "No question received."
        elif option == "summary":
            summarization = Summarization()
            return summarization.summarize(claim_data=self.claim_data)

        elif option == "analysis":
            holistic_analysis = HolisticAnalysis()
            holistic_analysis.analysis(patient_data=self.patient_data)
        else:
            print(f"Option {option} not available")


if __name__ == "__main__":
    pipeline = Pipeline(patient_id="PA-12345",claim_id="CLM153910000")
    print(pipeline.pipeline(option="summary"))
    print(f"\n")
    pipeline.pipeline(option="analysis")
    # print(pipeline.pipeline(option="advanced_qa",question="Who is the patient?"))
