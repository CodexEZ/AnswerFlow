import streamlit as st
from google import genai
from google.genai import types
import time


st.markdown("# Answer Flow")

uploaded_file = st.file_uploader("Upload a PDF File", type = ["pdf"])
API_KEY = st.secrets['API_KEY']
client = genai.Client(api_key=API_KEY)

if uploaded_file is not None:
    st.success("File uploaded successfully")
    file_bytes = uploaded_file.read()
    with st.spinner('Extracting Questions . . .',show_time = True):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents = [
                types.Part.from_bytes(
                    data = file_bytes,
                    mime_type="application/pdf",
                ),
                "Extract all the questions from the PDF and write down each question separated by newline, just give the questions do not write anything else other than that"
            ]
        )
    
    questions = response.text.split('\n')
    output_area = st.empty()  # Placeholder for updating the markdown
    print(questions.__len__())
    answer = ''
    with st.spinner('Generating answers ✍️ . . .', show_time = True):
        for num, question in enumerate(questions):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction='You are a helpful AI Tutor who has expertise in Natural Language Processing. Give answers to the questions and keep it relatively short and meaningful such that after reading it one can expand upon it.'
                ),
                contents=[f"{question}"]
            )
            answer += f'## Q{num+1} . {question}\n'
            answer += f'{response.text}\n'
            answer += '---\n'

            output_area.markdown(answer)
            time.sleep(2)
    with open('answers.md', 'w') as f:
        st.download_button(
        label="📥 Download Markdown File",
        data=f,
        file_name="answers.md",
        mime="text/markdown"
        )
