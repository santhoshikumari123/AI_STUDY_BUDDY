import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from pypdf import PdfReader


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error(
        "GROQ_API_KEY is missing. "
        "Please add it to your .env file."
    )
    st.stop()


# =========================================================
# GROQ CLIENT
# =========================================================

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-20b"


# =========================================================
# SESSION STATE
# =========================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0

if "quizzes_generated" not in st.session_state:
    st.session_state.quizzes_generated = 0

if "topics_summarized" not in st.session_state:
    st.session_state.topics_summarized = 0

if "uploaded_text" not in st.session_state:
    st.session_state.uploaded_text = ""


# =========================================================
# DARK / LIGHT MODE
# =========================================================

st.sidebar.markdown("## 🎨 Appearance")

dark_mode = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode
)

st.session_state.dark_mode = dark_mode


# =========================================================
# CUSTOM CSS
# =========================================================

if dark_mode:

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }

        section[data-testid="stSidebar"] {
            background-color: #161b22;
        }

        .stTextInput input,
        .stTextArea textarea {
            background-color: #21262d !important;
            color: white !important;
            border: 1px solid #444c56 !important;
        }

        .stSelectbox div {
            color: white;
        }

        .feature-card {
            background-color: #161b22;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #30363d;
            margin-bottom: 15px;
        }

        .big-title {
            font-size: 42px;
            font-weight: bold;
        }

        .subtitle {
            font-size: 18px;
            color: #b1bac4;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <style>

        .feature-card {
            background-color: #f5f7fa;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #dddddd;
            margin-bottom: 15px;
        }

        .big-title {
            font-size: 42px;
            font-weight: bold;
        }

        .subtitle {
            font-size: 18px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# AI FUNCTION
# =========================================================

def get_ai_response(prompt):

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# 📚 AI Study Buddy")

st.sidebar.caption(
    "Your personal AI-powered learning assistant"
)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📌 Choose Feature",
    [
        "🏠 Home",
        "💬 Ask Question",
        "📖 Summarize Topic",
        "📝 Generate Quiz",
        "🃏 Flashcards",
        "📅 Study Plan",
        "💻 Coding Interview",
        "📄 Study Notes",
        "📊 Progress"
    ]
)


# =========================================================
# HOME
# =========================================================

if menu == "🏠 Home":

    st.markdown(
        '<div class="big-title">📚 AI Study Buddy</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Your personal AI-powered learning assistant 🤖'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    st.info(
        "🎓 Learn smarter • Practice better • Prepare confidently"
    )

    st.markdown("## 🚀 What can I help you with?")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">

            <h3>💬 Ask Questions</h3>

            Ask any academic or technical
            question and get a simple explanation.

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="feature-card">

            <h3>🃏 Flashcards</h3>

            Convert any topic into
            quick revision flashcards.

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">

            <h3>📝 Generate Quizzes</h3>

            Practice with AI-generated
            multiple-choice questions.

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="feature-card">

            <h3>📅 Study Plan</h3>

            Generate a personalized
            study timetable.

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="feature-card">

            <h3>💻 Coding Interview</h3>

            Practice programming
            and technical interview questions.

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="feature-card">

            <h3>📄 Study Notes</h3>

            Upload notes and ask
            questions about them.

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.success(
        "💡 Tip: Start with 'Ask Question' and ask "
        "the AI to explain a difficult topic."
    )


# =========================================================
# ASK QUESTION
# =========================================================

elif menu == "💬 Ask Question":

    st.header("💬 Ask Your Question")

    question = st.text_area(
        "What do you want to learn?",
        placeholder="Example: Explain inheritance in Java with a simple example."
    )

    if st.button("🤖 Get Answer", use_container_width=True):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("AI is thinking... 🤔"):

                try:

                    answer = get_ai_response(
                        f"""
You are an AI Study Buddy for college students.

Answer the student's question in a simple,
clear and beginner-friendly way.

Follow these rules:

- Explain the concept clearly.
- Use simple language.
- Give examples where useful.
- Mention important points for exams.
- If the question is programming-related,
  include a small example.
- Avoid unnecessary complexity.

Student Question:
{question}
"""
                    )

                    st.session_state.questions_asked += 1

                    st.success("Answer")

                    st.write(answer)

                    st.session_state.chat_history.append(
                        {
                            "question": question,
                            "answer": answer
                        }
                    )

                except Exception as e:

                    st.error("Unable to get AI response.")
                    st.code(str(e))


# =========================================================
# SUMMARIZE
# =========================================================

elif menu == "📖 Summarize Topic":

    st.header("📖 Topic Summarizer")

    topic = st.text_area(
        "Enter the topic",
        placeholder="Example: Java OOP concepts"
    )

    summary_style = st.selectbox(
        "Summary Style",
        [
            "Exam Preparation",
            "Beginner Friendly",
            "Short Revision Notes",
            "Detailed Explanation"
        ]
    )

    if st.button("📖 Summarize", use_container_width=True):

        if not topic.strip():

            st.warning("Please enter a topic.")

        else:

            with st.spinner("Creating summary... ✍️"):

                try:

                    summary = get_ai_response(
                        f"""
You are an AI Study Buddy.

Create a {summary_style} summary
for the following topic.

Include:

1. Definition
2. Important concepts
3. Examples
4. Advantages or applications if relevant
5. Important exam points
6. Quick revision points

Topic:
{topic}
"""
                    )

                    st.session_state.topics_summarized += 1

                    st.success("📖 Summary")

                    st.write(summary)

                except Exception as e:

                    st.error("Unable to generate summary.")
                    st.code(str(e))


# =========================================================
# QUIZ
# =========================================================

elif menu == "📝 Generate Quiz":

    st.header("📝 AI Quiz Generator")

    quiz_topic = st.text_input(
        "Quiz Topic",
        placeholder="Example: Java Arrays"
    )

    difficulty = st.select_slider(
        "Difficulty",
        options=[
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    number = st.slider(
        "Number of Questions",
        3,
        10,
        5
    )

    if st.button("🧠 Generate Quiz", use_container_width=True):

        if not quiz_topic.strip():

            st.warning("Please enter a topic.")

        else:

            with st.spinner("Generating quiz... 🧠"):

                try:

                    quiz = get_ai_response(
                        f"""
You are an AI Study Buddy.

Create {number} multiple-choice questions
about {quiz_topic}.

Difficulty:
{difficulty}

For every question provide:

Question:
A)
B)
C)
D)

Correct Answer:
Explanation:

Make the questions useful for
college exams and placement preparation.
"""
                    )

                    st.session_state.quizzes_generated += 1

                    st.success("📝 Quiz")

                    st.write(quiz)

                except Exception as e:

                    st.error("Unable to generate quiz.")
                    st.code(str(e))


# =========================================================
# FLASHCARDS
# =========================================================

elif menu == "🃏 Flashcards":

    st.header("🃏 Flashcard Generator")

    topic = st.text_input(
        "Enter topic",
        placeholder="Example: SQL Joins"
    )

    count = st.slider(
        "Number of Flashcards",
        5,
        15,
        8
    )

    if st.button(
        "🃏 Create Flashcards",
        use_container_width=True
    ):

        if not topic.strip():

            st.warning("Please enter a topic.")

        else:

            with st.spinner("Creating flashcards..."):

                try:

                    cards = get_ai_response(
                        f"""
Create {count} study flashcards
for the topic: {topic}.

Format:

Card 1
Question:
Answer:

Card 2
Question:
Answer:

Keep answers short and useful
for quick revision.
"""
                    )

                    st.write(cards)

                except Exception as e:

                    st.error("Unable to create flashcards.")
                    st.code(str(e))


# =========================================================
# STUDY PLAN
# =========================================================

elif menu == "📅 Study Plan":

    st.header("📅 Personalized Study Planner")

    subjects = st.text_area(
        "Subjects",
        placeholder="Java, SQL, Aptitude, Reasoning, English"
    )

    hours = st.number_input(
        "Available study hours per day",
        min_value=1,
        max_value=12,
        value=3
    )

    days = st.number_input(
        "Number of days",
        min_value=1,
        max_value=60,
        value=7
    )

    goal = st.text_input(
        "Your goal",
        placeholder="Example: Prepare for campus placements"
    )

    if st.button(
        "📅 Create Study Plan",
        use_container_width=True
    ):

        if not subjects.strip():

            st.warning("Please enter your subjects.")

        else:

            with st.spinner("Creating your study plan..."):

                try:

                    plan = get_ai_response(
                        f"""
Create a personalized study plan.

Subjects:
{subjects}

Available hours per day:
{hours}

Number of days:
{days}

Goal:
{goal}

Create a realistic daily timetable.

Include:
- Study sessions
- Practice time
- Revision
- Breaks
- Mock tests
- Daily goals

Keep the plan suitable for a
college student preparing for placements.
"""
                    )

                    st.success("📅 Your Study Plan")

                    st.write(plan)

                except Exception as e:

                    st.error("Unable to create study plan.")
                    st.code(str(e))


# =========================================================
# CODING INTERVIEW
# =========================================================

elif menu == "💻 Coding Interview":

    st.header("💻 Coding & Technical Interview Practice")

    language = st.selectbox(
        "Programming Language",
        [
            "Java",
            "Python",
            "SQL",
            "JavaScript"
        ]
    )

    level = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    topic = st.text_input(
        "Topic",
        placeholder="Example: Arrays"
    )

    if st.button(
        "💻 Generate Interview Question",
        use_container_width=True
    ):

        with st.spinner("Preparing interview question..."):

            try:

                interview = get_ai_response(
                    f"""
Act as a technical interviewer.

Programming Language:
{language}

Difficulty:
{level}

Topic:
{topic}

Create one interview/coding question.

Provide:

1. Problem statement
2. Example input
3. Example output
4. Constraints
5. Hint

Do NOT provide the solution immediately.

After the student attempts it,
they can ask for the solution.
"""
                )

                st.write(interview)

            except Exception as e:

                st.error("Unable to generate question.")
                st.code(str(e))


# =========================================================
# STUDY NOTES
# =========================================================

elif menu == "📄 Study Notes":

    st.header("📄 Upload & Study Your Notes")

    st.write(
        "Upload a PDF or TXT file and ask questions "
        "about its contents."
    )

    uploaded_file = st.file_uploader(
        "Upload your notes",
        type=["pdf", "txt"]
    )

    if uploaded_file:

        try:

            if uploaded_file.name.endswith(".pdf"):

                reader = PdfReader(uploaded_file)

                text = ""

                for page in reader.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

            else:

                text = uploaded_file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

            st.session_state.uploaded_text = text

            st.success(
                f"✅ {uploaded_file.name} uploaded successfully!"
            )

            st.info(
                f"Extracted approximately "
                f"{len(text)} characters."
            )

        except Exception as e:

            st.error("Could not read this file.")
            st.code(str(e))

    if st.session_state.uploaded_text:

        question = st.text_area(
            "Ask something about your notes",
            placeholder="Example: What are the main points?"
        )

        if st.button(
            "🔍 Ask About Notes",
            use_container_width=True
        ):

            if not question.strip():

                st.warning("Please enter a question.")

            else:

                with st.spinner("Searching your notes..."):

                    try:

                        # Keep prompt reasonably sized
                        notes = st.session_state.uploaded_text[:50000]

                        answer = get_ai_response(
                            f"""
You are an AI Study Buddy.

Answer the student's question using
ONLY the provided study notes.

If the answer is not available in
the notes, clearly say:

"The answer is not available
in the uploaded notes."

Study Notes:
{notes}

Student Question:
{question}
"""
                        )

                        st.success("📚 Answer")

                        st.write(answer)

                    except Exception as e:

                        st.error("Unable to process notes.")
                        st.code(str(e))


# =========================================================
# PROGRESS
# =========================================================

elif menu == "📊 Progress":

    st.header("📊 Your Study Progress")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Questions Asked",
            st.session_state.questions_asked
        )

    with col2:

        st.metric(
            "Quizzes Generated",
            st.session_state.quizzes_generated
        )

    with col3:

        st.metric(
            "Topics Summarized",
            st.session_state.topics_summarized
        )

    st.markdown("---")

    st.subheader("💬 Recent Questions")

    if st.session_state.chat_history:

        for item in reversed(
            st.session_state.chat_history[-5:]
        ):

            with st.expander(
                item["question"]
            ):

                st.write(item["answer"])

    else:

        st.info(
            "Your questions will appear here."
        )

    st.markdown("---")

    if st.button(
        "🗑️ Clear Progress",
        use_container_width=True
    ):

        st.session_state.questions_asked = 0
        st.session_state.quizzes_generated = 0
        st.session_state.topics_summarized = 0
        st.session_state.chat_history = []

        st.success("Progress cleared!")


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "📚 AI Study Buddy | Built for Students 🎓 | "
    "Powered by Groq"
)