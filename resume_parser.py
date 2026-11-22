import os
import pymupdf
from docx import Document


class ResumeParser:

    def __init__(self):
        self.supported_formats = [".pdf", ".docx", ".txt"]

    def validate_file(self, file_path):

        if not os.path.isfile(file_path):
            raise FileNotFoundError("Resume file not found.")

        extension = os.path.splitext(file_path)[1].lower()

        if extension not in self.supported_formats:
            raise ValueError("Unsupported resume format.")

        if os.path.getsize(file_path) == 0:
            raise ValueError("The uploaded file is empty.")

        return extension

    def extract_pdf(self, file_path):

        extracted_text = []

        with pymupdf.open(file_path) as pdf:
            for page in pdf:
                extracted_text.append(page.get_text())

        return "\n".join(extracted_text)

    def extract_docx(self, file_path):

        document = Document(file_path)
        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)

    def extract_txt(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as file:
            return file.read()

    def parse_resume(self, file_path):

        extension = self.validate_file(file_path)

        if extension == ".pdf":
            text = self.extract_pdf(file_path)

        elif extension == ".docx":
            text = self.extract_docx(file_path)

        else:
            text = self.extract_txt(file_path)

        if not text.strip():
            raise ValueError("No readable text found in the resume.")

        return text