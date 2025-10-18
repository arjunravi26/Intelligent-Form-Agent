from src.pipeline import Pipeline
import sys


def run():
    try:
        arg_count = len(sys.argv) - 1
        if arg_count < 1:
            print("Usage: python -m main <option> [question]")
            print("  <option>   : required argument (e.g., 'qa', 'summary')")
            print("  [question] : optional argument (string, e.g., 'What is diagnosis?')")

            sys.exit(1)

        option = sys.argv[1]
        question = " ".join(sys.argv[2:]) if arg_count > 1 else ""

        pipeline = Pipeline(patient_id="PA-12345", claim_id="CLM153910000") # You can change patient_id and claim_id with any other id in data/claim folder
        print(pipeline.pipeline(option=option, question=question))

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()

