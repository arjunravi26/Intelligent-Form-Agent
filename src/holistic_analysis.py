from collections import defaultdict

class HolisticAnalysis:
    def __init__(self):
        pass

    def analysis(self,data):
        total_copay = sum(claim['financials']['copay'] for claim in data)
        total_allowed_amount = sum(claim['financials']['allowed_amount'] for claim  in data)
        total_insurance_paid = sum(claim['financials']['insurance_paid'] for claim  in data)
        providers = set(claim['provider_name'] for claim in data)
        diagnosis_counts = defaultdict(int)
        total_claims_count = len(data)
        for claim in data:
            diagnosis_counts[claim['primary_diagnosis']] += 1


        print(f"Print Holistic Report for Patient {patient_data[0]['patient_info']['first_name']} {patient_data[0]['patient_info']['last_name']} with Patient id {patient_data[0]['patient_info']['patient_id']}")
        print(f"Total Copay: {total_copay}")
        print(f"Total Allowed amount: {total_allowed_amount}")
        print(f"Total Insurance paid: {total_insurance_paid}")
        print(f"Provider names: {providers}")
        print(f"Diagnosis count: {diagnosis_counts}")
        print(f"No of times claim requested: {total_claims_count}")


    def analyze_with_llm(self):
        pass


if __name__ == "__main__":
    from src.data_ingestion import DataIngestion
    data_ingestion = DataIngestion(patient_id="PA-12345")
    patient_data = data_ingestion.ingest_patient_data()
    # print(patient_data)
    holistic_analysis = HolisticAnalysis()
    holistic_analysis.analysis(patient_data)

