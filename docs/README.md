# Intelligent Form Agent

[](https://opensource.org/licenses/Apache-2.0)
[](https://www.python.org/)

## Overview

The **Intelligent Form Agent** is a powerful tool designed to **process and understand digital forms** (e.g., medical claims, financial reports). It automatically extracts information from both **structured fields** (like JSON data or labeled entries) and **unstructured free-form text**. The agent then utilizes this aggregated data to answer user questions, produce concise summaries, and generate holistic insights when analyzing multiple forms collectively.

The agent’s core capabilities are:

  * **Data Extraction:** Reading and parsing form data, combining structured (JSON) and unstructured (Text) components.
  * **Question Answering (QA):** Responding to user queries about a single form's content using both **Extractive** (Basic) and **Abstractive/Reasoning** (Advanced) methods.
  * **Summarization:** Producing brief, narrative summaries highlighting the most important details of a form.
  * **Multi-Form Analysis:** Aggregating and synthesizing information across multiple forms to provide holistic patient/subject reports.

-----

## 🛠️ Setup Instructions

Follow these steps to set up your environment and install the necessary dependencies.

### Prerequisites

  * **Python 3.7+**
  * **Git**
  * (Optional but highly recommended) A **virtual environment** (using `venv` or `conda`).

### 1\. Clone the Repository

Clone the project from GitHub and navigate into the directory:

```bash
git clone https://github.com/arjunravi26/Intelligent-Form-Agent.git
cd Intelligent-Form-Agent
```

### 2\. Install Dependencies

Install all required Python libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3\. Configuration & API Key

  * Edit the **`config.yaml`** file to specify model names or paths.

  * Create a **`.env`** file in the root directory and configure your **Hugging Face API Token** as an environment variable (required for model access):

    ```
    HF_TOKEN="<Your-HuggingFace-API-Key>"
    ```

### 4\. Data Placement

  * Ensure your sample form files (JSON and TXT pairs) are placed within the **`/data`** directory (e.g., `data/claim/`) or use the available sample data provided.

-----

## 🚀 Usage Guide

The agent is executed via the Python module system from the command line, using the `main` script and specific options.

### Running the Agent

**Command Structure:**

```bash
python -m main <OPTION> "<Your question>"
```

| OPTION | Functionality | Question Required? |
| :--- | :--- | :--- |
| `qa` | Basic Extractive QA (Single Form) | **YES** |
| `advanced_qa` | Advanced Abstractive QA (Single Form) | **YES** |
| `summary` | Generates a Summary (Single Form) | NO |
| `analysis` | Holistic Multi-Form Report | NO |

## 💡 Example Queries and Expected Outputs

The following examples simulate the agent's behavior across its core functions using the sample data.

### 1\. Basic Question Answering (Extractive QA)

**Input:**

```bash
python -m main qa "who is doctor?"
```

**Agent Output:**

```
Output: Dr. David Chen
```

### 2\. Advanced Question Answering (Abstractive QA with Reasoning)

**Input:**

```bash
python -m main advanced_qa "who is doctor?"
```

**Agent Output:**

```
Output: Answer: 'Dr. David Chen',
Reason: "The answer can be found in the 'provider_name' field of the claim details, which states: 'provider_name': 'Dr. David Chen (Pulmonology)'. This indicates that Dr. David Chen is the provider, and since he is mentioned as seeing the patient, it can be inferred that he is the doctor."
```

### 3\. Generating a Summary of One Form (Summarization)

**Input:**

```bash
python -m main summary
```

**Agent Output:**

```
Output: “SummarizationOutput(summary_text='Patient Katelyn Whitaker (Policy: P49924-54) was seen today, 2025-07-17, by Dr. David Chen (Pulmonology). The main subjective complaint was a recurrent flare-up of their **Asthma** symptoms, which are generally well-managed. Assessment determined the necessity of a diagnostic procedure to confirm the severity: Spirometry (Lung Function Test) (CPT: 94010). The diagnosis code assigned is **J45.909**.')”
```

### 4\. Providing a Holistic Report Across Multiple Forms (Multi-Form Analysis)

**Input:**

```bash
python -m main analysis
```

**Agent Output:**

```
Output: “Print Holistic Report for Patient Katelyn Whitaker with Patient id PA-12345
Total Copay: 225.0
Total Allowed amount: 6102.94
Total Insurance paid: 5877.94
Provider names: {'Dr. Ava Sharma (Cardiology)', 'Dr. David Chen (Pulmonology)'}
Diagnosis count: defaultdict(<class 'int'>, {'Asthma': 1, 'Hypertension': 3})
No of times claim requested: 4”
```

*(Note: This report aggregates all structured data available for Patient PA-12345 in the `/data/claim` directory.)*

-----

## ⚙️ Design Notes: Pipeline / Architecture

The system operates using a modular pipeline to process raw forms into structured knowledge for answering queries. The core differentiator is the use of **Generative AI (LLMs)** for abstractive reasoning and complex analysis.

### System Pipeline

1.  **Input Processing & Context Creation:**

      * Ingests form documents (JSON/TXT pairs).
      * **Combines both structured data** (`claim_details.json`) with **unstructured data** (`claim_text_data.txt`) into a unified context.
      * Cleans and formats data for optimal input to Large Language Models.

2.  **Question Answering Module - Basic (`qa`):**

      * Relies on a fine-tuned **Extractive Model** to precisely locate and return the answer from the context span.

3.  **Question Answering Module - Advanced (`advanced_qa`):**

      * Employs an **Abstractive Model/LLM** with a strict output format (JSON) to not only generate the `Answer` but also provide a logical, reasoned explanation (`Reason`) based on the input data.

4.  **Summarization Pipeline (`summary`):**

      * Utilizes a dedicated **Summarization Model** or an LLM prompted for summary generation using the full context.

5.  **Multi-Form Analysis (`analysis`):**

      * Iterates and **aggregates information** specifically from the **structured data** across all patient documents.
      * Synthesizes key metrics (totals, counts, unique values) to produce a **Holistic Report**.

This modular architecture ensures that all core functions are powered by a unified data layer and leverages the specific strengths of various **Gen AI and NLP models** for distinct tasks (extraction, abstraction, and synthesis).

## Conclusion and Contribution
The Intelligent Form Agent moves beyond simple data capture, providing a robust pipeline for transforming raw form documents into actionable business intelligence. By integrating advanced extractive and abstractive models, the agent ensures that complex questions are answered with both precision and reasoning, and that insights across multiple claims are synthesized effectively.

We encourage you to clone the repository, follow the Setup Instructions, and experiment with the various modes (qa, advanced_qa, summary, and analysis).