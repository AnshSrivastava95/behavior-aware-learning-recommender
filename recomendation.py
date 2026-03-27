
import google.generativeai as genai
from tkinter import Tk, filedialog
from content_input import pdf_read, extract_topics
from secrets import API_KEY


genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

student_profile = {
    "strategy": "focused",
    "prefered_modality": "visual",
    "prefered_difficulty": 0.65
}


# Hide main window
root = Tk()
root.withdraw()

# Open file picker
file_path = filedialog.askopenfilename(
    title="Select Syllabus PDF",
    filetypes=[("PDF Files", "*.pdf")]
)

if file_path:

    text = pdf_read(file_path)
    topics = extract_topics(text)
else:
    print("No file selected")

def generate_focused(profile, unit):

    pref = profile["prefered_difficulty"]
    modality = profile["prefered_modality"]

    return [
        {"unit": unit, "modality": modality, "difficulty": round(pref - 0.1, 2)},
        {"unit": unit, "modality": modality, "difficulty": round(pref, 2)},
        {"unit": unit, "modality": modality, "difficulty": round(pref + 0.1, 2)},
        {"unit": unit, "modality": "challenge", "difficulty": round(pref + 0.25, 2)}
    ]


def generate_hybrid(profile, unit):

    pref = profile["prefered_difficulty"]

    return [
        {"unit": unit, "modality": "visual", "difficulty": round(pref - 0.15, 2)},
        {"unit": unit, "modality": "quiz", "difficulty": round(pref - 0.05, 2)},
        {"unit": unit, "modality": "practice", "difficulty": round(pref + 0.05, 2)},
        {"unit": unit, "modality": "revision", "difficulty": round(pref, 2)}
    ]


def generate_content(profile, unit):

    if profile["strategy"] == "focused":
        return generate_focused(profile, unit)

    elif profile["strategy"] == "hybrid":
        return generate_hybrid(profile, unit)

    else:
        raise ValueError("Unknown strategy")

def build_prompt(step, profile, syllabus_text):

    return f"""
You are an expert computer science tutor.

Student prefers: {profile['prefered_modality']} learning.

Topic: {step['unit']}
Modality: {step['modality']}
Difficulty: {step['difficulty']}

Use the following syllabus context:
{syllabus_text[:1000]}

Instructions:
- Stay strictly within syllabus
- Generate relevant content only
- Practice → problem
- Quiz → 3 MCQs with answers
- Visual → explanation
- Revision → short notes
- Challenge → advanced problem

Keep it structured and clear.
"""

def generate_with_gemini(step, profile,syllabus_text):

    try:
        prompt = build_prompt(step, profile,syllabus_text)

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"
    
learning_path = generate_content(student_profile, "memory_management")

for step in learning_path:
    print("\n====================")
    print("STEP:", step)

    content = generate_with_gemini(step, student_profile,text)

    print("CONTENT:\n", content)