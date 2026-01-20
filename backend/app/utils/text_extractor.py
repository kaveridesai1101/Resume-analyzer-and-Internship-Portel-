import io
from pdfminer.high_level import extract_text
from docx import Document

def extract_text_from_binary(content: bytes, filename: str) -> str:
    """
    Extracts text from PDF, DOCX, or plain text files.
    """
    if not filename:
        return content.decode("utf-8", errors="ignore")
        
    extension = filename.split('.')[-1].lower()
    
    try:
        if extension == 'pdf':
            return extract_text(io.BytesIO(content))
        elif extension == 'docx':
            doc = Document(io.BytesIO(content))
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        else:
            # Fallback to UTF-8 decoding for .txt or unknown extensions
            return content.decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Error extracting text from {filename}: {e}")
        # Final fallback
        return content.decode("utf-8", errors="ignore")
