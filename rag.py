# from pypdf import PdfReader
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np
# import ollama

# pdf_path = "SpCVE.pdf"

# reader = PdfReader(pdf_path)

# text = ""
# for page in reader.pages:
#     page_text = page.extract_text()
#     if page_text:
#         text += page_text

# def chunk_text(text, chunk_size=500):
#     return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# chunks = chunk_text(text)

# model = SentenceTransformer("all-MiniLM-L6-v2")

# embeddings = model.encode(chunks)
# embeddings = np.array(embeddings, dtype=np.float32)

# index = faiss.IndexFlatL2(embeddings.shape[1])
# index.add(embeddings)


# def ask_resume(question):

#     query_embedding = model.encode([question])
#     query_embedding = np.array(query_embedding, dtype=np.float32)

#     D, I = index.search(query_embedding, k=3)

#     context = ""

#     for idx in I[0]:
#         context += chunks[idx] + "\n"

#     prompt = f"""
#     Resume Content:
#     {context}

#     Question:
#     {question}

#     Answer only from the resume.
#     """

#     response = ollama.chat(
#         model="llama3",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     return response["message"]["content"]
# from pypdf import PdfReader
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np
# import ollama
# import re

# # =====================================
# # CONFIG
# # =====================================

# PDF_PATH = "raj-sarkar-resume (1).pdf"

# # =====================================
# # LOAD RESUME
# # =====================================

# try:
#     reader = PdfReader(PDF_PATH)

#     text = ""

#     for page in reader.pages:
#         page_text = page.extract_text()

#         if page_text:
#             text += page_text + "\n"

# except Exception:
#     text = ""

# # =====================================
# # CHUNKING
# # =====================================

# def chunk_text(text, chunk_size=500):

#     return [
#         text[i:i + chunk_size]
#         for i in range(0, len(text), chunk_size)
#     ]

# chunks = chunk_text(text)

# # =====================================
# # EMBEDDING MODEL
# # =====================================

# try:

#     model = SentenceTransformer(
#         "all-MiniLM-L6-v2"
#     )

#     if len(chunks) > 0:

#         embeddings = model.encode(
#             chunks
#         )

#         embeddings = np.array(
#             embeddings,
#             dtype=np.float32
#         )

#         index = faiss.IndexFlatL2(
#             embeddings.shape[1]
#         )

#         index.add(
#             embeddings
#         )

#     else:

#         index = None

# except Exception:

#     model = None
#     index = None

# # =====================================
# # RAG RETRIEVAL
# # =====================================

# def retrieve_context(question, k=5):

#     if index is None:
#         return ""

#     query_embedding = model.encode(
#         [question]
#     )

#     query_embedding = np.array(
#         query_embedding,
#         dtype=np.float32
#     )

#     distances, indices = index.search(
#         query_embedding,
#         k
#     )

#     context = ""

#     for idx in indices[0]:

#         if idx < len(chunks):
#             context += chunks[idx] + "\n"

#     return context

# # =====================================
# # RESUME CHAT
# # =====================================

# def ask_resume(question):

#     context = retrieve_context(question)

#     prompt = f"""
# Resume Content:

# {context}

# Question:
# {question}

# Rules:
# - Answer only from resume.
# - Do not hallucinate.
# - If answer not found say:
#   Not found in resume.
# """

#     response = ollama.chat(
#         model="llama3",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     return response["message"]["content"]

# # =====================================
# # ATS ANALYSIS
# # =====================================

# def analyze_resume():

#     if not text:
#         return "No resume loaded."

#     prompt = f"""
# You are an ATS Expert.

# Analyze this resume:

# {text}

# Target Role:
# Computer Vision Engineer

# Provide:

# 1. ATS Score /100
# 2. Resume Summary
# 3. Technical Skills Found
# 4. Missing Skills
# 5. Strengths
# 6. Weaknesses
# 7. ATS Improvements
# 8. Recommended Certifications
# 9. Recommended Projects
# 10. Career Growth Plan

# Return ATS score as percentage.
# """

#     response = ollama.chat(
#         model="llama3",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     return response["message"]["content"]

# # =====================================
# # SKILL GROWTH
# # =====================================

# def skill_growth():

#     if not text:
#         return "No resume loaded."

#     prompt = f"""
# Analyze this resume:

# {text}

# Candidate Goal:
# Computer Vision Engineer

# Provide:

# 1. Current Skills
# 2. Missing Skills
# 3. Beginner Skills
# 4. Intermediate Skills
# 5. Advanced Skills
# 6. Certifications
# 7. Projects
# 8. Salary Roadmap
# 9. 6 Month Learning Plan
# 10. Interview Topics
# """

#     response = ollama.chat(
#         model="llama3",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     return response["message"]["content"]

# # =====================================
# # RESUME BUILDER
# # =====================================

# def generate_resume(
#     template,
#     name,
#     email,
#     phone,
#     role,
#     skills,
#     experience,
#     projects,
#     education,
#     certifications
# ):

#     prompt = f"""
# Create a professional ATS optimized resume.

# Template:
# {template}

# Name:
# {name}

# Email:
# {email}

# Phone:
# {phone}

# Role:
# {role}

# Skills:
# {skills}

# Experience:
# {experience}

# Projects:
# {projects}

# Education:
# {education}

# Certifications:
# {certifications}

# Requirements:

# - Professional Summary
# - Technical Skills
# - Work Experience
# - Projects
# - Education
# - Certifications
# - ATS Keywords
# - Modern formatting

# Return markdown resume.
# """

#     response = ollama.chat(
#         model="llama3",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     return response["message"]["content"]

# # =====================================
# # RESUME IMPROVEMENT
# # =====================================

# def improve_resume():

#     if not text:
#         return "No resume loaded."

#     prompt = f"""
# Improve this resume:

# {text}

# Provide:

# 1. Better Summary
# 2. Better Experience Points
# 3. ATS Keywords
# 4. Missing Skills
# 5. Certifications
# 6. Projects
# 7. Improved Resume Version
# """

#     response = ollama.chat(
#         model="llama3",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     return response["message"]["content"]

# # =====================================
# # JD MATCH
# # =====================================

# def jd_match(job_description):

#     prompt = f"""
# Resume:

# {text}

# Job Description:

# {job_description}

# Provide:

# 1. ATS Match %
# 2. Matching Skills
# 3. Missing Skills
# 4. Suggested Keywords
# 5. Resume Improvements
# 6. Interview Areas
# """

#     response = ollama.chat(
#         model="llama3",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     return response["message"]["content"]

# # =====================================
# # AUTO-FILL FROM UPLOADED RESUME
# # =====================================

# def extract_resume_data(resume_text):

#     data = {
#         "name": "",
#         "email": "",
#         "phone": "",
#         "skills": ""
#     }

#     email_match = re.search(
#         r'[\w\.-]+@[\w\.-]+',
#         resume_text
#     )

#     if email_match:
#         data["email"] = email_match.group()

#     phone_match = re.search(
#         r'(\+91)?[0-9]{10}',
#         resume_text
#     )

#     if phone_match:
#         data["phone"] = phone_match.group()

#     lines = resume_text.split("\n")

#     if len(lines) > 0:
#         data["name"] = lines[0]

#     return data


"""
rag.py
------------------------------------
Multi-PDF Retrieval Augmented Generation
"""

import os
import uuid

import fitz  # PyMuPDF

import chromadb

from sentence_transformers import SentenceTransformer

from langchain.text_splitter import RecursiveCharacterTextSplitter

from chatbot import bot

from prompts import RAG_PROMPT

from config import VECTOR_DB


class RAG:

    def __init__(self):

        self.documents = []

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path=VECTOR_DB
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    # =====================================
    # Read PDF
    # =====================================

    def read_pdf(self, pdf):

        if isinstance(pdf, str):

            document = fitz.open(pdf)

        else:

            document = fitz.open(
                stream=pdf.read(),
                filetype="pdf"
            )

        text = ""

        for page in document:

            text += page.get_text()

        document.close()

        return text

    # =====================================
    # Chunk Text
    # =====================================

    def chunk_text(self, text):

        return self.splitter.split_text(text)

    # =====================================
    # Add PDF to Vector DB
    # =====================================

    def add_document(self, pdf_path):

        text = self.read_pdf(pdf_path)

        chunks = self.chunk_text(text)

        for chunk in chunks:

            embedding = self.embedding_model.encode(
                chunk
            ).tolist()

            self.collection.add(

                ids=[str(uuid.uuid4())],

                documents=[chunk],

                embeddings=[embedding]

            )

        self.documents.append(pdf_path)

        return True
        # =====================================
    # Retrieve Relevant Chunks
    # =====================================

    def retrieve(self, question, top_k=4):

        embedding = self.embedding_model.encode(
            question
        ).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )

        documents = []

        if results["documents"]:

            documents = results["documents"][0]

        return documents

    # =====================================
    # Build Context
    # =====================================

    def build_context(self, question):

        docs = self.retrieve(question)

        if not docs:
            return ""

        return "\n\n".join(docs)

    # =====================================
    # Ask Question
    # =====================================

    def ask(self, question):

        context = self.build_context(question)

        if context.strip():

            prompt = RAG_PROMPT.format(
                context=context,
                question=question
            )

        else:

            prompt = f"""
No document context was found.

Answer the following question using your general knowledge.

Question:
{question}
"""

        answer = bot.chat(prompt)

        return answer

    # =====================================
    # Search Only
    # =====================================

    def search(self, query):

        return self.retrieve(query)

    # =====================================
    # Count Documents
    # =====================================

    def count(self):

        return len(self.documents)

    # =====================================
    # Reset Vector Store
    # =====================================

    def clear(self):

        try:

            self.client.delete_collection("documents")

        except Exception:
            pass

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

        self.documents = []

    # =====================================
    # List Uploaded PDFs
    # =====================================

    def list_documents(self):

        return self.documents


# ==========================================
# Singleton
# ==========================================

rag = RAG()