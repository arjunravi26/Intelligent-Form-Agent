# Intelligent Form Agent

## Overview

The **Intelligent Form Agent** is a powerful tool designed to **process and understand digital forms**. It automatically extracts information from both **structured fields** (like tables or labeled entries) and **unstructured free-form text**. The agent then utilizes this extracted data to answer user questions, produce concise summaries, and generate holistic insights when analyzing multiple forms collectively.

The agent’s core capabilities are:

  * **Data Extraction:** Reading and parsing form data.
  * **Question Answering (QA):** Responding to user queries about a single form's content both basic and advanced QA.
  * **Summarization:** Producing brief summaries highlighting the most important details of a form.
  * **Multi-Form Analysis:** Aggregating information across multiple forms to summarize the data.

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

### 3\. Configuration

* Edit the `config.yaml` file to set up required parameters:

    * Specify model names or paths.

* Create `.env` file to set up API TOKEN for huggingface:

    * Configure any necessary **API keys** as HF_TOKEN.

### 4\. Data Placement

  * Ensure your sample form files are placed within the **`/data`** directory (e.g., `data/claim/`) or use available data from `data/claim/`.

-----

## Usage Guide

The agent is run from the command line, allowing you to specify forms and queries.

### Running the Agent

The agent is executed via the `main.py` script. The specific arguments will depend on the script design (e.g., file path, query, mode).

#### Example Command Structure

```bash
python -m main "<Option>" "<Your question>"
```

**Options** are `[qa, advanced_qa, summary, analysis]`
**Question** are only for `qa` and `advanced_qa`
-----

## 💡 Example Queries and Expected Outputs

The following examples simulate the agent's behavior across its core functions.

### 1\. Answering a Question from a Single Form (Single-Form QA)

**Input:**

  `python -m main qa who is doctor?`

**Agent Output:**

```
Output: QuestionAnsweringOutputElement(answer='Dr. David Chen', end=227, score=0.008877340704202652, start=213)
```
### 2\. Answering a Question from a Single Form (Single-Form QA) - Advanced-QA

**Input:**

  `python -m main advanced_qa who is doctor?`

**Agent Output:**

```
Output: Answer: 'Dr. David Chen',
Reason: "The answer can be found in the 'provider_name' field of the claim details, which states: 'provider_name': 'Dr. David Chen (Pulmonology)'. This indicates that Dr. David Chen is the provider, and since he is mentioned as seeing the patient, it can be inferred that he is the doctor."

```
### 3\. Generating a Summary of One Form (Summarization)

**Input:**

  `python -m summary`

**Agent Output:**

```
Output: “SummarizationOutput(summary_text='Patient Katelyn Whitaker (Policy: P49924-54) was seen today, 2025-07-17, by Dr. David Chen (Pulmonology). The main subjective complaint was a recurrent flare-up of their **Asthma** symptoms, which are generally well-managed. Assessment determined the necessity of a diagnostic procedure to confirm the severity: Spirometry (Lung Function Test) (CPT: 94010). The diagnosis code assigned is **J45.909**.')”
```

### 4\. Providing a Holistic Answer Across Multiple Forms (Multi-Form Analysis)

**Input:**

  `python -m main analysis`

**Agent Output:**

```
Output: “Print Holistic Report for Patient Katelyn Whitaker with Patient id PA-12345
Total Copay: 225.0
Total Allowed amount: 6102.9400000000005
Total Insurance paid: 5877.9400000000005
Provider names: {'Dr. Ava Sharma (Cardiology)', 'Dr. David Chen (Pulmonology)'}
Diagnosis count: defaultdict(<class 'int'>, {'Asthma': 1, 'Hypertension': 3})
No of times claim requested: 4”
```

-----

## ⚙️ Design Notes: Pipeline / Architecture

The system operates using a modular pipeline to process raw forms into structured knowledge for answering queries.

### System Pipeline

1.  **Input Processing:**
      * Ingests form documents from `data\claim`.
      * Combine both structured data(claim_details.json) with unstructured data(claim_text_data.txt)
      * Clean data for giving to LLM Models, convert dict data into str.

2.  **Question Answering Module - Basic:**
      * For a single-form query, extract both structured and unstructured data from corresponding folder and create context..
      * An **Extractive model** extract correct answer for the question from the context.
3.  **Question Answering Module - Advanced:**
      * For a single-form query, extract both structured and unstructured data from corresponding folder and create context..
      * An **Abstractive model** with strict output as json generate both answer and it's reason for that answer as json.
4.  **Summarization Pipeline:**
      * An **Summarization model** with context of both structured and unstructured data we create summary of the data.
      * These details are constructed into a concise narrative summary.
5.  **Multi-Form Analysis:**
      * The **aggregates information** across all provided documents(structured data) of a patient.
      * It synthesizes the results to answer queries that require comparison, counting, or other collective insights.

This modular architecture ensures that all core functions (Extraction, QA, Summarization, Multi-Form Analysis) are powered by a unified Gen AI, Analysis layer, which can utilize modern tools like powerful LLM APIs.