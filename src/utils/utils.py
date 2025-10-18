from typing import Dict


def process_data(data: Dict):
    try:
        details_str = "\n".join(
            f"{key}: {value}" for key, value in data.items() if key != "Clinical_note")
        context = f"{details_str}\nClinical Note:\n{data.get('Clinical_note', '')}"
        return context
    except Exception as e:
        print(f"Raise Exception {e}")
        return None
