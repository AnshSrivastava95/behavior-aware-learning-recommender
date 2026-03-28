import streamlit as st
from groq import Groq
from content_input import pdf_read, extract_topics
from config import API_KEY
import tempfile
import time

# ---------------- SETUP ----------------
client = Groq(api_key=API_KEY)

def generate_with_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ---------------- PROMPT ----------------
def build_prompt(topic, modality, text):
    return f"""
You are an expert tutor.

Teach topic: {topic}

Student prefers: {modality}

Use syllabus:
{text[:1200]}

Explain clearly with structure.
"""


# ---------------- MCQ ----------------
def generate_mcqs(topic):
    prompt = f"""
Generate 3 MCQs on topic: {topic}.

STRICT FORMAT:

Q1: Question
A) option
B) option
C) option
D) option
Answer: A
"""
    return generate_with_llm(prompt)


def parse_mcqs(text):
    lines = text.split("\n")
    questions = []
    current_q = {}

    for line in lines:
        line = line.strip()

        if line.startswith("Q"):
            if current_q:
                questions.append(current_q)
            current_q = {"question": line, "options": [], "answer": ""}

        elif line.startswith(("A)", "B)", "C)", "D)")):
            current_q["options"].append(line)

        elif line.startswith("Answer"):
            current_q["answer"] = line.split(":")[1].strip()

    if current_q:
        questions.append(current_q)

    return questions


# ---------------- UI ----------------
st.set_page_config(page_title="AI Learning System", layout="wide")

st.title("📚 Adaptive AI Learning System")

uploaded_file = st.file_uploader("Upload Syllabus PDF", type="pdf")

if uploaded_file:

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name

    text = pdf_read(path)
    topics = extract_topics(text)

    st.subheader("📌 Extracted Topics")
    for t in topics:
        st.write("-", t)

    # ---------------- INIT SESSION ----------------
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.stage = "testing"
        st.session_state.style_index = 0
        st.session_state.styles = ["visual", "practice", "quiz"]
        st.session_state.scores = {}
        st.session_state.mcqs = []
        st.session_state.q_index = 0
        st.session_state.current_score = 0
        st.session_state.best_style = None
        st.session_state.history = []

    unit1_topic = topics[0]

    # ---------------- TESTING PHASE ----------------
    if st.session_state.stage == "testing":

        # Move to final if done
        if st.session_state.style_index >= len(st.session_state.styles):
            st.session_state.stage = "final"
            st.rerun()

        current_style = st.session_state.styles[st.session_state.style_index]

        st.subheader(f"📖 Learning ({current_style})")

        prompt = build_prompt(unit1_topic, current_style, text)
        content = generate_with_llm(prompt)
        st.write(content)

        if st.button("Start Test"):

            mcq_text = generate_mcqs(unit1_topic)
            st.session_state.mcqs = parse_mcqs(mcq_text)

            if not st.session_state.mcqs:
                st.error("Failed to generate MCQs. Try again.")
                st.rerun()

            st.session_state.stage = "quiz"
            st.session_state.q_index = 0
            st.session_state.current_score = 0
            st.rerun()

    # ---------------- QUIZ ----------------
    elif st.session_state.stage == "quiz":

        # SAFE CHECK
        if st.session_state.q_index >= len(st.session_state.mcqs):

            score = (st.session_state.current_score / len(st.session_state.mcqs)) * 10

            style = st.session_state.styles[st.session_state.style_index]
            st.session_state.scores[style] = score

            st.success(f"{style} Score: {score:.2f}")

            st.session_state.style_index += 1
            st.session_state.stage = "testing"
            st.session_state.q_index = 0
            st.session_state.current_score = 0

            st.rerun()

        q_data = st.session_state.mcqs[st.session_state.q_index]

        st.subheader(q_data["question"])

        for opt in q_data["options"]:
            if st.button(opt):

                selected = opt[0]
                correct = q_data["answer"]

                if selected == correct:
                    st.success("Correct ✅")
                    st.session_state.current_score += 1
                else:
                    st.error(f"Wrong ❌ (Correct: {correct})")

                time.sleep(1)  # smooth transition

                st.session_state.q_index += 1
                st.rerun()

    # ---------------- FINAL (CONTINUOUS MODE) ----------------
    elif st.session_state.stage == "final":

        if st.session_state.best_style is None:
            best_style = max(st.session_state.scores, key=st.session_state.scores.get)
            st.session_state.best_style = best_style

        best_style = st.session_state.best_style

        st.success(f"🎯 Best Learning Style: {best_style}")

        # 📊 Chart
        st.subheader("📊 Style Performance")
        st.bar_chart(st.session_state.scores)

        # 📚 History
        st.subheader("📚 Learning History")
        st.write(st.session_state.history)

        st.subheader("📖 Continuous Learning Mode")

        topic = st.text_input("Enter topic to learn")

        if topic:
            st.session_state.history.append(topic)

            prompt = build_prompt(topic, best_style, text)
            content = generate_with_llm(prompt)

            st.subheader(f"📘 Learning: {topic}")
            st.write(content)

        # Restart
        if st.button("🔄 Restart System"):
            st.session_state.clear()
            st.rerun()