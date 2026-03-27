import pandas as pd
import google.generativeai as genai

genai.configure(api_key="AIzaSyANgndoSuBctEJmWBgi7EGyic-ZvkD8pP0")
model = genai.GenerativeModel("models/gemini-2.5-flash")
content_db = pd.read_csv("content.csv")

student_profile = {
    "strategy": "focused",
    "prefered_modality": "visual",
    "prefered_difficulty": 0.65
}


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



def build_prompt(step, profile):

    return f"""
You are an expert computer science tutor.

Student prefers: {profile['prefered_modality']} learning.

Generate content for:

Topic: {step['unit']}
Modality: {step['modality']}
Difficulty: {step['difficulty']}

Rules:
- Practice → create a problem
- Quiz → create 3 MCQs with answers
- Visual → intuitive explanation
- Revision → short notes
- Challenge → difficult problem

Keep it clear, structured, and student-friendly.
"""
def generate_with_gemini(step, profile):

    try:
        prompt = build_prompt(step, profile)

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"
    
learning_path = generate_content(student_profile, "memory_management")

for step in learning_path:
    print("\n====================")
    print("STEP:", step)

    content = generate_with_gemini(step, student_profile)

    print("CONTENT:\n", content)