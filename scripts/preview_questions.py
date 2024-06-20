import streamlit as st
import json

# Load the JSON file
with open('/home/dica/Projects/syvan_projects/pdf_parser/pdf_parser/paper_exams/questions2.json') as f:
    questions = json.load(f)

# Iterate over the questions
for question in questions:
    # st.write(f"Question Title: {question['question_title']}")
    # st.write(f"Original Text: {question['original_text']}")
    # st.write(f"Quiz Options: {question['quiz_options']}")
    # st.write(f"Correct Option: {question['correct_option']}")
    # st.write(f"Question Type: {question['question_type']}")
    # st.write(f"Explanation: {question['explanation']}")
    # st.write("---")
    st.write(f"Question Title: {question['question_title']}")
    st.write(f"Original Text: {question['original_text']}")
    st.write(f"Quiz Options: {question['quiz_options']}")
    st.write(f"Correct Option: {question['correct_option']}")
    st.write(f"Question Type: {question['question_type']}")
    st.write(f"Explanation: {question['explanation']}")
    st.write("---")