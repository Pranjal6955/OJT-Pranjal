# OJT Journal Maker

A **Daily Activity Journal PDF Auto-Filler** powered by Google Gemini AI. Upload your OJT (On-the-Job Training) PDF template, describe your internship work, and the app intelligently splits it into per-day entries, generates professional journal content, and fills every page of your PDF—automatically.

---

## ✨ Features

- **AI-Powered Content Generation** – Google Gemini 1.5 Flash writes realistic, professional daily journal entries based on your overall work description.
- **Smart Work Splitting** – Automatically divides your internship work across all working days (Mon–Fri), respecting holidays/skip dates.
- **PDF Template Filling** – Overlays generated text onto your existing PDF template using coordinate detection and text-label scanning.
- **3-Step Wizard UI** – Clean dark-themed single-page app: upload → review → download.
- **Editable Previews** – Review and edit AI-generated daily work before PDF generation.
- **Progress Tracking** – Real-time progress bar while the PDF is being generated in the background.

---

## 🗂 File Structure

```
OJT-maker/
├── main.py             # FastAPI backend (API endpoints + background task)
├── gemini_helper.py    # Google Gemini API integration
├── pdf_filler.py       # PDF overlay filling (PyMuPDF + ReportLab + PyPDF2)
├── requirements.txt    # Python dependencies
├── static/
│   └── index.html      # Single-page frontend (vanilla HTML/CSS/JS)
└── README.md
```

---

## ⚙️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Sign in with your Google account.
3. Click **Create API Key**.
4. Copy the key – you'll paste it into the app's form.

### 3. Run the Server

```bash
uvicorn main:app --reload
```

The app will be available at **http://localhost:8000**.

---

## 🚀 How to Use

### Step 1 – Upload & Configure
1. Open **http://localhost:8000** in your browser.
2. Drag-and-drop (or click to upload) your OJT journal **PDF template**.
3. Fill in:
   - **Start Date / End Date** – your internship period.
   - **Skip Dates** *(optional)* – holidays or leave days, comma-separated (e.g. `2024-12-25, 2025-01-01`).
   - **OJT Timing** – e.g. `8:00 AM – 5:00 PM`.
   - **Department** and **Designation**.
   - **Work Description** – a paragraph or more describing everything you did during the internship.
   - **Gemini API Key** – your key from Google AI Studio.
4. Click **Upload & Process**. Gemini will split your work description into daily tasks.

### Step 2 – Review Daily Work
- A scrollable list of day cards appears, one per working day.
- Each card shows the date and an editable textarea with the AI-generated work for that day.
- Edit any entry as needed.
- Click **✨ Generate PDF** when ready.

### Step 3 – Generate & Download
- A progress bar tracks each journal entry being generated and filled into the PDF.
- When complete, click **⬇️ Download PDF** to save your finished journal.
- Click **↩ Start Over** to begin a new session.

---

## 🛠 Tech Stack

| Layer     | Technology |
|-----------|-----------|
| Backend   | FastAPI, Uvicorn |
| AI        | Google Gemini 1.5 Flash (`google-generativeai`) |
| PDF Read  | PyMuPDF (`fitz`) |
| PDF Write | ReportLab + PyPDF2 |
| Frontend  | Vanilla HTML / CSS / JavaScript |

---

## 📝 Notes

- The app fills PDFs using a **text overlay** strategy. It first tries to detect field labels in the PDF, then falls back to hardcoded A4 coordinate positions.
- If the PDF template has more pages than working days, the last journal entry is repeated.
- All processing is done locally except for the Gemini API calls.
