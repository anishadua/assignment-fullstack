from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fitz  # PyMuPDF
import os
import openai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    document_id: str
    question: str

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    file_location = f"files/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    text = extract_text_from_pdf(file_location)
    text_file_location = f"text_files/{file.filename}.txt"
    with open(text_file_location, "w") as text_file:
        text_file.write(text)
    return JSONResponse(content={"filename": file.filename, "text": text})

@app.post("/question/")
async def answer_question(request: QuestionRequest):
    document_id = request.document_id
    question = request.question
    text_file_location = f"text_files/{document_id}.txt"
    if not os.path.exists(text_file_location):
        raise HTTPException(status_code=404, detail="Document not found")
    with open(text_file_location, "r") as f:
        text = f.read()
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable for API key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{question}\n\n{text}",
        max_tokens=150
    )
    answer = response.choices[0].text.strip()
    return JSONResponse(content={"answer": answer})


