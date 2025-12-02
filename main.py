from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

print("Groq key loaded:", bool(GROQ_API_KEY))
print("Groq model:", GROQ_MODEL)

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set in .env or environment variables.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

app = FastAPI(
    title="AI Test Case Suggester (Groq)",
    description="Generates test case suggestions using Groq LLM based on PR diffs.",
    version="1.0.0",
)

class GenerateRequest(BaseModel):
    diff: str
    language: Optional[str] = "python"
    framework: Optional[str] = "pytest"

class GenerateResponse(BaseModel):
    suggestions_markdown: str


def build_prompt(diff: str, language: str, framework: str) -> str:
    return f"""
You are an expert SDET and backend engineer.

Here is a Git diff from a pull request. Analyze it and generate:

1. Unit test cases (inputs & expected outputs)
2. Edge cases & boundary tests
3. If applicable: API/integration test scenarios
4. Suggest example test function names or code skeletons.

Use language: {language}, test framework: {framework}.
Return the answer in GitHub Markdown format.

---
Git Diff:
\"\"\"diff
{diff}
\"\"\"diff
"""


def call_groq_for_tests(diff: str, language: str, framework: str) -> str:
    prompt = build_prompt(diff, language, framework)
    print("DEBUG: calling Groq with model:", GROQ_MODEL)

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant specialized in software testing."
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        print("DEBUG: got response from Groq")
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error while calling Groq API:", repr(e))
        raise HTTPException(status_code=500, detail=f"Groq API error: {e}")


@app.post("/generate-tests", response_model=GenerateResponse)
def generate_tests(payload: GenerateRequest):
    suggestions = call_groq_for_tests(
        diff=payload.diff,
        language=payload.language,
        framework=payload.framework,
    )
    return GenerateResponse(suggestions_markdown=suggestions)


@app.get("/")
def root():
    return {"message": "AI Test Suggester is running"}
