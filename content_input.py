from PyPDF2 import PdfReader

def pdf_read(file_path):
    reader = PdfReader(file_path)

    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text


def extract_topics(text):
    lines=text.split("\n")
    topics=[]
    for line in lines:
        line=line.strip()
        if not line:
            continue
        if "SECTION" in line.upper():
            continue
        if len(line.split())>6:
            continue
        topics.append(line)
    return topics
