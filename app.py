import streamlit as st
from google import genai
from google.genai import types
import time

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

# Upload section
uploaded_file = st.file_uploader("📄 Upload a PDF File", type=["pdf"])

# Set your API key securely
API_KEY = st.secrets['API_KEY']
client = genai.Client(api_key=API_KEY)

if uploaded_file is not None:
    st.success("✅ File uploaded successfully")
    file_bytes = uploaded_file.read()

    with st.spinner('🔍 Extracting Questions...'):
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
                    system_instruction='You are a helpful AI Tutor who has expertise in Natural Language Processing. Give answers to the questions and keep it relatively short and meaningful such that after reading it one can expand upon it.'
                ),
                contents=[f"{question}"]
            )

            answer += f'## ❓ Q{num+1}: {question}\n'
            answer += f'🧠 **Answer**: {response.text}\n'
            answer += '---\n'

            output_area.markdown(answer, unsafe_allow_html=True)
            time.sleep(1.5)

    st.markdown("### 📥 Download the complete answer set:")
    st.download_button(
        label="📄 Download Markdown File",
        data=answer,
        file_name="answers.md",
        mime="text/markdown"
    )
    uploaded_file = None
