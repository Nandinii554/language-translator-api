# 📄 PDF Translation API

The **PDF Translation API** is a FastAPI-based web application that enables automated language detection and translation of textual content from PDF files. Users can upload a PDF document, have its language detected using machine learning (FastText), and receive a translated version of the document in a user-specified output format: `JSON`, `TXT`, `DOCX`, or `PDF`.

This project demonstrates the integration of NLP (Natural Language Processing), file parsing, and translation services in a practical application. It can be used for multilingual document processing, translation workflows, or as a backend microservice in larger systems.

---

## 🚀 Features

### 🔍 Automatic Language Detection
- Utilizes **FastText**'s `lid.176.ftz` model trained on 176 languages for robust language identification.
- Detects the predominant language from the extracted text of a PDF.
- Returns both the **language name**, **ISO code**, and **confidence score**.

### 🌐 Seamless Translation
- Employs **GoogleTranslator** (via `deep-translator`) for high-quality and efficient translation.
- Supports translation across **100+ languages**, making it suitable for global content workflows.

### 📤 Multi-format Output
Choose from a variety of output formats to best suit your downstream application needs:
- **JSON** – Best for integrations, APIs, and downstream text analysis.
- **TXT** – Lightweight plain text version for human-readable storage or scripts.
- **DOCX** – Structured output in Microsoft Word format using `python-docx`.
- **PDF** – Cleanly formatted PDF output rendered via `reportlab`.

### 🖥️ Easy-to-use API Interface
- Built on **FastAPI**, known for its high performance and intuitive developer experience.
- Comes with **interactive Swagger UI** (`/docs`) and **ReDoc UI** (`/redoc`) for real-time testing and API documentation.
- Error handling and file validation built-in for smooth user experience.

---

## 🖼️ Screenshots

### 1. 🌐 API User Interface (Swagger UI)

Below is the screenshot of the interactive FastAPI Swagger UI used to test the `/translate-pdf` endpoint:

![image](https://github.com/user-attachments/assets/9010ec1e-cdb2-4d98-9b09-21d2433837ce)

---

### 2. 📄 Translated PDF Output (Example: French)

Here is a sample of a translated PDF output with content converted from English to French:

![Screenshot 2025-06-16 at 6 31 29 PM](https://github.com/user-attachments/assets/38a1c1c6-a94a-4973-a3f8-00609dd9c123)
