import google.generativeai as genai
import json
import re
import time
from datetime import datetime


# ─────────────────────────────────────────────
# ✅ DATE FORMATTER
# ─────────────────────────────────────────────
def format_date(date_str: str) -> str:
    try:
        for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%y"]:
            try:
                parsed = datetime.strptime(date_str, fmt)
                return parsed.strftime("%-d-%-m-%Y")
            except ValueError:
                continue
        return date_str
    except Exception:
        return date_str


# ─────────────────────────────────────────────
# ✅ SAFE GEMINI CALL (handles 429)
# ─────────────────────────────────────────────
def call_gemini(model, prompt, retries=3):
    for i in range(retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.4,
                    "top_p": 0.9,
                }
            )
            text = response.text.strip()
            text = re.sub(r'^```(?:json)?\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            return text

        except Exception as e:
            if "429" in str(e):
                time.sleep(40)
            else:
                raise e
    raise Exception("Gemini failed after retries")


# ─────────────────────────────────────────────
# ✅ SPLIT WORK INTO DAYS (IMPROVED PROMPT)
# ─────────────────────────────────────────────
def split_work_into_days(api_key: str, work_description: str, dates: list, num_days: int) -> list:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
You are a professional OJT training supervisor.

Divide the following work into EXACTLY {num_days} day-wise entries.

RULES:
- No HR / meetings / company talk
- Only technical/project work
- Each day must be unique
- Maintain progression:
  understanding → planning → implementation → debugging → improvement
- Each day: 2–4 meaningful sentences
- No generic phrases
- No repetition
- No empty or incomplete entries
- Use college/student-level tools (avoid professional tools like Jira, Azure, enterprise software)

OUTPUT JSON ONLY:
[
  {{ "day": 1, "work": "..." }}
]

WORK:
{work_description}
"""

    text = call_gemini(model, prompt)

    daily_splits = json.loads(text)

    result = []
    for i, item in enumerate(daily_splits[:num_days]):
        formatted_date = format_date(dates[i]) if i < len(dates) else ""
        result.append({
            "day": i + 1,
            "date": formatted_date,
            "work": item["work"]
        })

    return result


# ─────────────────────────────────────────────
# ✅ GENERATE ALL JOURNAL ENTRIES IN ONE CALL 🚀
# ─────────────────────────────────────────────
def generate_all_journals(api_key: str, daily_data: list) -> list:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    combined_input = "\n".join([
        f"Day {d['day']} ({d['date']}): {d['work']}"
        for d in daily_data
    ])

    prompt = f"""
Generate professional OJT daily journal entries for college students.

RULES:
- Each day must be unique
- No repetition
- No HR/company content
- BE EXTREMELY CONCISE. Use short phrases.
- Use bullet points (prefix with "• ") for multi-line fields.
- Avoid professional/enterprise tools (no Jira, Azure, Salesforce, etc.)
- Use college-friendly tools: Python, JavaScript, Git, SQL, VS Code, Linux, React, etc.

For EACH day return:
- my_space: ONE short sentence of reflection (max 15 words)
- tasks_carried_out: 2-3 short bullet points (each max 8 words)
- key_learnings: 2-3 short bullet points (each max 8 words)
- tools_used: comma-separated list (max 4 tools)
- special_achievements: ONE short sentence (max 12 words) (NEVER "N/A")

OUTPUT JSON (use plain text with newlines for multi-line fields):
[
  {{
    "day": 1,
    "my_space": "reflection text",
    "tasks_carried_out": "• Task 1\\n• Task 2",
    "key_learnings": "• Learning 1\\n• Learning 2",
    "tools_used": "Tool, Tool",
    "special_achievements": "achievement text"
  }}
]

INPUT:
{combined_input}
"""

    text = call_gemini(model, prompt)

    return json.loads(text)


# ─────────────────────────────────────────────
# ✅ FINAL PIPELINE FUNCTION
# ─────────────────────────────────────────────
def generate_full_entries(api_key: str, work_description: str, dates: list):
    num_days = len(dates)

    # Step 1: Split
    daily_split = split_work_into_days(api_key, work_description, dates, num_days)

    # Step 2: Generate ALL entries (1 API call)
    journal_data = generate_all_journals(api_key, daily_split)

    # Merge
    final = []
    for i in range(num_days):
        entry = journal_data[i]
        base = daily_split[i]

        final.append({
            "date_display": base["date"],
            "my_space": entry["my_space"],
            "tasks_carried_out": entry["tasks_carried_out"],
            "key_learnings": entry["key_learnings"],
            "tools_used": entry["tools_used"],
            "special_achievements": entry["special_achievements"],
        })

    return final


# ─────────────────────────────────────────────
# ✅ SINGLE JOURNAL ENTRY (for backward compatibility)
# ─────────────────────────────────────────────
def generate_journal_entry(api_key: str, date: str, work: str) -> dict:
    """Generate structured journal entry for one day using Gemini."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Format date to DD-M-YYYY
    formatted_date = format_date(date)

    prompt = f"""Generate a professional internship daily journal entry for a college student.

Date: {formatted_date}
Work Done: {work}

Return ONLY a valid JSON object:
{{
  "my_space": "ONE short sentence of reflection (max 15 words)",
  "tasks_carried_out": "• Task 1\\n• Task 2\\n• Task 3",
  "key_learnings": "• Learning 1\\n• Learning 2",
  "tools_used": "tool1, tool2, tool3 (max 4 tools)",
  "special_achievements": "ONE short sentence (max 12 words)"
}}

IMPORTANT:
- Use college/student-level tools only (Python, JavaScript, Git, VS Code, Linux, React, etc.)
- BE EXTREMELY CONCISE. Use bullet points (• ) for lists.
- Each task/learning should be a short phrase.
- Total lines per field should not exceed 3-4."""

    text = call_gemini(model, prompt)
    return json.loads(text)