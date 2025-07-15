import fitz  # PyMuPDF

def extract_text_from_pdf(file_stream):
    doc = fitz.open(stream=file_stream, filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text
