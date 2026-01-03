import streamlit as st
import fitz 
import spacy
import nltk
import re
import random
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")
def extract_text_from_pdf(pdf_file):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text
def clean_text(text):
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
def extract_concepts(text):
    doc = nlp(text)
    concepts = []
    for sent in doc.sents:
        if len(sent.text.split()) > 6:
            concepts.append(sent.text)
    return concepts
def generate_1_mark(concepts):
    questions = []
    for c in concepts:
        questions.append(f"Define {c.split()[0]}.")
    return questions
def generate_2_mark(concepts):
    questions = []
    for c in concepts:
        questions.append(f"Explain {c.split()[0]} briefly.")
    return questions
def generate_5_mark(concepts):
    questions = []
    for c in concepts:
        questions.append(f"Explain {c.split()[0]} with advantages.")
    return questions
def generate_8_mark(concepts):
    questions = []
    for c in concepts:
        questions.append(f"Explain {c.split()[0]} in detail with diagram.")
    return questions
st.set_page_config(page_title="Exam Question Generator", layout="wide")
st.title("Intelligent Exam Question Generator (NLP)")
st.subheader("Upload syllabus / notes PDF and generate exam questions")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")
mark_type = st.selectbox("Select Marks",
                          ["1 Mark", "2 Mark", "5 Mark", "8 Mark"])
difficulty = st.selectbox("Difficulty Level",
                           ["Easy", "Medium", "Hard"])
num_questions = st.slider("Number of Questions", 5, 30, 10)
if uploaded_file:
    raw_text = extract_text_from_pdf(uploaded_file)
    cleaned_text = clean_text(raw_text)
    concepts = extract_concepts(cleaned_text)
    concepts = random.sample(concepts, min(len(concepts), num_questions))
    st.success("PDF processed successfully!")
    if st.button("Generate Questions"):
        if mark_type == "1 Mark":
            qs = generate_1_mark(concepts)
        elif mark_type == "2 Mark":
            qs = generate_2_mark(concepts)
        elif mark_type == "5 Mark":
            qs = generate_5_mark(concepts)
        else:
            qs = generate_8_mark(concepts)
        st.subheader("Generated Questions")
        for i, q in enumerate(qs, 1):
            st.write(f"{i}. {q}")
