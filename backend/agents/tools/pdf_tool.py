import os
import PyPDF2
from crewai.tools import tool

# ---------------------------------------------------------
# CUSTOM CREWAI TOOL: Local PDF Reader
# ---------------------------------------------------------
# DESIGN RATIONALE: We built a custom PyPDF2 tool instead of using off-the-shelf
# web-based PDF readers to ensure that potentially sensitive study materials
# are processed strictly locally before the extracted text is sent to the LLM.

@tool("Read Local PDF File")
def read_local_pdf_file(file_path: str) -> str:
    """Reads and extracts text from a local PDF document.
    Use this tool to extract all the text content from the study materials.
    """
    # Guard clause: Ensure the file was saved correctly by the FastAPI backend
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    try:
        text_content = ""
        # Open in binary mode for PyPDF2
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            
            # Iterate through all pages to capture the full context of the document.
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_content += extracted + "\n"
        
        # Edge Case Handling: Some PDFs are purely scanned images with no OCR text layer.
        if not text_content.strip():
            return f"Warning: The PDF at {file_path} appears to be empty or consists only of unreadable images."
            
        return text_content
        
    except Exception as e:
        # Graceful failure: Return the error to the agent so it can decide how to proceed,
        # rather than crashing the entire backend process.
        return f"Error reading PDF: {str(e)}"
