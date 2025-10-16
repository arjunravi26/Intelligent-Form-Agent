from faker import Faker
from typing import List, Dict
import pandas as pd
import random
import os

fake = Faker()

JOBS: Dict[str, List[str]] = {
    "AI Engineer": [
        "LLM", "HuggingFace", "GPT", "Transformer", "RAG", "Finetuning",
        "LoRa", "QLoRa", "Quantization", "Fastapi", "Git", "Docker", "Agent",
        "Langchain", "vLLm", "TGI", "API development", "Multi-Agent",
        "Multi-Model", "Chatbot", "Voice-AI", "Whisper", "TTS", "Unsloth"
    ],
    "Data Scientist": [
        "Python", "SQL", "Statistics", "Machine Learning", "Deep Learning",
        "NLP", "Pandas", "Numpy", "Scikit-learn", "Matplotlib", "Seaborn",
        "TensorFlow", "PyTorch", "Tableau", "PowerBI", "Data Preprocessing",
        "Feature Engineering", "Model Evaluation", "Big Data (Spark/Hadoop)"
    ],
    "Software Engineer": [
        "Python", "Java", "C++", "Algorithms", "Data Structures",
        "OOP", "Databases", "REST API", "Microservices", "Git", "Docker",
        "Unit Testing", "CI/CD", "Agile Methodologies"
    ],
    "Front-end Engineer": [
        "HTML", "CSS", "JavaScript", "TypeScript", "React", "Vue.js",
        "Next.js", "Bootstrap", "Tailwind CSS", "Responsive Design",
        "REST API Integration", "Git"
    ],
    "Backend Engineer": [
        "Python", "Java", "Node.js", "Django", "Flask", "Spring Boot",
        "SQL", "NoSQL", "Microservices", "REST API", "GraphQL", "Docker", "Git"
    ],
    "DevOps": [
        "Linux", "Shell Scripting", "AWS", "Azure", "GCP", "Docker", "Kubernetes",
        "Terraform", "CI/CD", "Jenkins", "Git", "Monitoring (Prometheus, Grafana)"
    ],
    "QA Engineer": [
        "Manual Testing", "Automation Testing", "Selenium", "JUnit", "PyTest",
        "Cypress", "Postman", "API Testing", "Performance Testing",
        "CI/CD", "Bug Tracking (JIRA)"
    ]
}

ABOUT_ME_TEMPLATES: List[str] = [
    "I am a passionate {job} with {exp} years of experience specializing in {skill}. I enjoy solving complex problems and working in {industry}.",
    "As a {job}, I have a strong background in {skill}, and I am eager to contribute my expertise to innovative projects.",
    "With {exp} years in {industry}, I have honed my skills in {skill}. I value teamwork and continuous learning."
]

INDUSTRIES: List[str] = ["finance", "healthcare",
                         "e-commerce", "AI research", "retail"]
BASE_DIR: str = "data/samples/job_applicants"

os.makedirs(BASE_DIR,exist_ok=True)

def create_applicant():
    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    job_applied = random.choice(list(JOBS.keys()))
    skills = ", ".join(random.sample(JOBS[job_applied], k=5))
    years_exp = random.randint(1, 10)
    industry = random.choice(INDUSTRIES)
    current_salary = random.randint(5,24)
    expected_salary = f"{random.randint(current_salary,current_salary * 3)} LPA"
    current_salary = f"{current_salary} LPA"
    about_me = random.choice(ABOUT_ME_TEMPLATES).format(
        job=job_applied,
        exp=years_exp,
        skill=skills,
        industry=industry
    )
    return {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Job Applied": job_applied,
        "Industry": industry,
        "Skills": skills,
        "Current Salary":current_salary,
        "Expected Salary":expected_salary,
        "Years of Experience": years_exp,
        "About Me": about_me
    }

def save_applicant_to_txt(applicant: Dict[str, str], directory: str = BASE_DIR) -> None:
    safe_name = applicant["Name"].replace(" ", "_")
    file_path = os.path.join(directory, f"{safe_name}.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        for key, value in applicant.items():
            f.write(f"{key}: {value}\n")


def generate_applicants(no_of_applicants:int=25):
    applicants = [create_applicant() for _ in range(no_of_applicants)]
    for applicant in applicants:
        save_applicant_to_txt(applicant=applicant)


if __name__ == "__main__":
    generate_applicants()


