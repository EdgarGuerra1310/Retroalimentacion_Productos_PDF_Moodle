import pdfplumber

def transcribir_pdf(pdf_path):
    texto = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texto += page.extract_text() or ""
    return texto.strip()