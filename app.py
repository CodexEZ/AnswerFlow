import streamlit as st
from google import genai
from google.genai import types
import time
from io import BytesIO
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section
# Page config
st.set_page_config(page_title="Answer Flow", page_icon="💡", layout="wide")

st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #000000;
            color: white;
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }

        /* Optional: change link hover or image styling inside sidebar */
        [data-testid="stSidebar"] img {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)
# Sidebar
with st.sidebar:
    st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcm5la3ZtZG55eW84cWExMHM4dTk2YXZpdG0xYXprbm8xY255dWkzcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PjJ1cLHqLEveXysGDB/giphy.gif", width=200)
    st.markdown("### 🤖 AI Answer Bot")
    st.markdown("Upload a **PDF** and get smart, concise answers!")
    st.markdown("---")
    st.caption("Built with 💛 using Streamlit + Gemini API")

# Main header
st.markdown("<h1 style='text-align: center; color: #4F8BF9;'>📘 Answer Flow</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Let AI extract & answer questions from your PDFs</h4>", unsafe_allow_html=True)
st.markdown("---")
answer_length = st.radio(
    "📝 Select answer length:",
    ["Short", "Long"],
    index=0,
    horizontal=True
)
# Upload section

education_fields = [
    "Computer Science / IT",
    "Data Science / AI / Machine Learning",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Environmental Science",
    "Statistics",
    "Engineering (General)",
    "Mechanical Engineering",
    "Electrical Engineering",
    "Civil Engineering",
    "Electronics & Communication",
    "Aerospace Engineering",
    "Chemical Engineering",
    "Architecture",
    "Business Administration (BBA/MBA)",
    "Marketing",
    "Finance",
    "Accounting",
    "Human Resource Management",
    "Operations & Supply Chain",
    "Entrepreneurship",
    "International Business",
    "Economics",
    "History",
    "Political Science",
    "Sociology",
    "Psychology",
    "Philosophy",
    "Anthropology",
    "Linguistics",
    "Literature",
    "Education",
    "Gender Studies",
    "Religious Studies",
    "Journalism / Mass Communication",
    "Constitutional Law",
    "International Law",
    "Corporate Law",
    "Criminology",
    "Public Administration",
    "Public Policy",
    "Medicine (MBBS/MD)",
    "Nursing",
    "Pharmacy",
    "Dentistry",
    "Public Health",
    "Nutrition & Dietetics",
    "Biotechnology",
    "Physiotherapy",
    "Fine Arts",
    "Performing Arts (Dance, Music, Theatre)",
    "Graphic Design",
    "Animation",
    "Fashion Design",
    "Interior Design",
    "English",
    "French",
    "Spanish",
    "German",
    "Japanese",
    "Chinese",
    "Regional Languages",
    "Comparative Literature",
    "Artificial Intelligence",
    "Cybersecurity",
    "Game Design & Development",
    "Digital Marketing",
    "Ethical Hacking",
    "UX/UI Design",
    "Philosophy of Science",
    "Cognitive Science"
]

selected_field = st.selectbox("🎓 Choose your education field:", education_fields)
uploaded_file = st.file_uploader("📄 Upload a PDF File", type=["pdf"])

# Set your API key securely
API_KEY = st.secrets['API_KEY']
client = genai.Client(api_key=API_KEY)

if uploaded_file is not None:
    st.success("✅ File uploaded successfully")
    file_bytes = uploaded_file.read()

    with st.spinner('🔍 Extracting Questions...', show_time = True):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(
                    data=file_bytes,
                    mime_type="application/pdf",
                ),
                "Extract all the questions from the PDF and write down each question separated by newline, just give the questions do not write anything else other than that. Make sure the questions are separated perfectly such that no questions are split in two by accident"
            ]
        )

    questions = response.text.strip().split('\n')
    output_area = st.empty()
    answer = ''
    with st.spinner('✍️ Generating Answers...'):
        for num, question in enumerate(questions):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction = (
                        f"You are a helpful AI Tutor with expertise in {selected_field}. "
                        "Give answers to the questions in a clear, concise way, suitable for quick understanding."
                        if answer_length == "Short" else
                        f"You are a helpful AI Tutor with expertise in {selected_field}. "
                        "Give in-depth, detailed answers to the questions, elaborating on important concepts and examples where necessary."
                    )
                ),
                contents=[f"{question}"]
            )

            answer += f'## ❓ Q{num+1}: {question}\n'
            answer += f'🧠 **Answer**:\n\n{response.text}\n'
            answer += '---\n'

            output_area.markdown(answer, unsafe_allow_html=True)
            time.sleep(2)

    st.markdown("### 📥 Download the complete answer set:")
    pdf = MarkdownPdf(toc_level=1)
    pdf.add_section(Section(answer, toc=0))
    buffer = BytesIO()
    pdf.save(buffer)
    buffer.seek(0)
    st.download_button(
        label="📄 Download Markdown File",
        data=buffer,
        file_name="answers.pdf",
        mime="text/markdown"
    )
    uploaded_file = None
