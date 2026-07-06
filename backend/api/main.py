from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Form
import shutil
import os
import tempfile
from agents.study_crew import create_study_workflow
from pydantic import BaseModel
from typing import Optional

# ---------------------------------------------------------
# FASTAPI APP INITIALIZATION
# ---------------------------------------------------------
# This acts as the backend microservice orchestration layer.
app = FastAPI(title="LearnSync API", description="AI Study Concierge Backend", version="1.0.0")

class AnalysisResponse(BaseModel):
    result: str

@app.get("/")
def read_root():
    return {"message": "Welcome to LearnSync API. Send a POST request with a PDF to /analyze-pdf"}

# ---------------------------------------------------------
# CORE ANALYSIS ENDPOINT
# ---------------------------------------------------------
@app.post("/analyze-pdf", response_model=AnalysisResponse)
def analyze_pdf(
    file: UploadFile = File(...), 
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    model: str = Form("gemini/gemini-2.5-flash")
):
    # SECURITY IMPLEMENTATION: Ensure API Key is passed via headers (not query params)
    # to avoid logging keys in standard server access logs.
    if not x_api_key:
        raise HTTPException(
            status_code=401, 
            detail="API Key is missing. Please provide it via X-API-Key header."
        )
        
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # SECURITY IMPLEMENTATION: File Size Limitation (Max 15 MB)
    # This prevents Denial of Service (DoS) attacks via massively inflated PDFs 
    # overloading the memory or exhausting the local disk space.
    MAX_FILE_SIZE = 15 * 1024 * 1024
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail="File size exceeds the maximum limit of 15 MB. Please upload a smaller document."
        )
    
    # ---------------------------------------------------------
    # WORKFLOW EXECUTION
    # ---------------------------------------------------------
    # Save uploaded file to a secure temporary location. 
    # tempfile ensures unique naming to prevent concurrency collisions.
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        # Trigger the CrewAI multi-agent workflow
        result = create_study_workflow(tmp_path, api_key=x_api_key, model=model)
        
        return {"result": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # CLEANUP: Ensure the temp file is deleted regardless of success or failure.
        # This prevents disk space exhaustion on the host server.
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except:
                pass
