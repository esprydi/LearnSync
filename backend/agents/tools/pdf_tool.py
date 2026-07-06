import os
import PyPDF2
from crewai.tools import tool

@tool("Read Local PDF File")
def read_local_pdf_file(file_path: str) -> str:
    """Reads and extracts text from a local PDF document.
    Use this tool to extract all the text content from the study materials.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    try:
        text_content = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_content += extracted + "\n"
        
        if not text_content.strip():
            return f"Warning: The PDF at {file_path} appears to be empty or consists only of unreadable images."
            
        return text_content
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
