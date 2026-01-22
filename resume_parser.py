import os
import json
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


client = Groq(api_key = os.getenv("GROQ_API_KEY"))

def extract_resume_data(text):
    prompt = """
    Return ONLY valid JSON.
Rules:
- No explanations
- No markdown
- Use double quotes
- No trailing commas
- If a field is missing, use "Not Found"

Schema:
{
  "Full Name": "",
  "Contact Information": {
    "Email": "",
    "Phone Number": ""
  },
  "Education": [],
  "Skills": {
    "Technical Skills": {},
    "Soft Skills": ""
  },
  "Work Experience": [],
  "Projects": []
}"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages = [
            {"role": "system","content":"You are a strict JSON generator."},
            {"role": "user", "content":text+prompt},
        ],
        temperature = 0
    )

    answer_text = response.choices[0].message.content

    print("RAW AI o/p:",answer_text)


    start_index = answer_text.find("{")
    end_index = answer_text.rfind("}")

    if start_index == -1 and end_index == -1:
        raise ValueError("No JSON object found")
    clean_json_string = answer_text[start_index:end_index + 1]
    data = json.loads(clean_json_string)
    skills = data.get("Skills", {}).get("Technical Skills", {})
    for k, v in skills.items():
        if isinstance(v, str):
            skills[k] = [x.strip() for x in v.split(",")]
    return data
    
    






if __name__ == "__main__":
    resume_text = """
    Alex R. Coder
    (+1) 555-0199-283 # alex.coder.dev@example.com 
    
    Education
    University of Technology, San Francisco
    Bachelor of Science in Computer Science (GPA: 3.8/4.0)
    May 2020 - May 2024
    
    Work Experience
    TechFlow Solutions Inc.
    Junior AI Engineer | June 2024 - Present
    • Developed a Python-based RAG pipeline processing 10k+ PDF documents daily.
    • Optimized API costs by 40% using caching strategies in Redis and LangChain.
    • Built internal dashboards using Streamlit to visualize model performance metrics.
    
    DataCorp Intern
    Summer 2023
    • Assisted in migrating on-premise SQL databases to AWS RDS.
    • Wrote Python scripts to automate data cleaning for 500GB of log files.
    
    Projects
    "Chat-with-PDF" Tool
    • Built a desktop app using PyQt and OpenAI API to summarize legal contracts.
    • Implemented vector search using ChromaDB to retrieve relevant clauses.
    
    Technical Skills
    • Languages: Python, JavaScript, SQL, Bash
    • Frameworks: React, FastAPI, LangChain
    • Tools: Git, Docker, VS Code, AWS
    """
    data = extract_resume_data(resume_text)
    print(data)
