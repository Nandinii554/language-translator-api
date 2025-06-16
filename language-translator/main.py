def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def save_to_docx(text: str, filename: str):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)

def save_to_pdf(text: str, filename: str):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    lines = text.split('\n')
    y = height - 50
    for line in lines:
        for subline in split_text(line, max_chars=90):
            c.drawString(50, y, subline)
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50
    c.save()

def split_text(text, max_chars=90):
    # Splits text into chunks that fit within max_chars
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

@app.post("/translate-pdf")
async def translate_pdf(
    file: UploadFile = File(...),
    target_lang: str = Form(...),
    output_format: str = Form("pdf")  # default: PDF
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    if output_format.lower() not in ["json", "txt", "docx", "pdf"]:
        raise HTTPException(status_code=400, detail="Invalid output format. Choose from: json, txt, docx, pdf.")

    try:
        temp_filename = f"temp_{uuid.uuid4().hex}.pdf"
        with open(temp_filename, "wb") as f:
            f.write(await file.read())

        # Extract text
        text = extract_text_from_pdf(temp_filename)
        os.remove(temp_filename)

        if not text:
            raise HTTPException(status_code=400, detail="The PDF contains no extractable text.")

        # Detect language
        predictions = model.predict(text.replace("\n", " "))
        label = predictions[0][0].replace("__label__", "")
        confidence = round(predictions[1][0], 2)
        lang_name = language_names.get(label, "Unknown")

        # Translate full text
        translated_text = GoogleTranslator(source=label, target=target_lang.strip()).translate(text)

        if output_format == "json":
            return JSONResponse({
                "detected_language": lang_name,
                "language_code": label,
                "confidence": confidence,
                "translated_to": target_lang,
                "translated_text": translated_text
            })

        elif output_format == "txt":
            txt_path = f"translated_{uuid.uuid4().hex}.txt"
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(translated_text)
            return FileResponse(txt_path, media_type="text/plain", filename="translated.txt")

        elif output_format == "docx":
            docx_path = f"translated_{uuid.uuid4().hex}.docx"
            save_to_docx(translated_text, docx_path)
            return FileResponse(docx_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename="translated.docx")

        elif output_format == "pdf":
            pdf_path = f"translated_{uuid.uuid4().hex}.pdf"
            save_to_pdf(translated_text, pdf_path)
            return FileResponse(pdf_path, media_type="application/pdf", filename="translated.pdf")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
