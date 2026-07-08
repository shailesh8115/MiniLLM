# from pypdf import PdfReader
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np
# import ollama

# # -------------------------
# # LOAD PDF
# # -------------------------
# pdf_path = "SpCVE.pdf"

# reader = PdfReader(pdf_path)

# text = ""

# for page in reader.pages:
#     page_text = page.extract_text()

#     if page_text:
#         text += page_text + "\n"


# # -------------------------
# # CHUNKING
# # -------------------------
# def chunk_text(text, chunk_size=500):

#     chunks = []

#     for i in range(0, len(text), chunk_size):
#         chunks.append(text[i:i + chunk_size])

#     return chunks


# chunks = chunk_text(text)

# print("Chunks:", len(chunks))


# # -------------------------
# # EMBEDDINGS
# # -------------------------
# model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )

# embeddings = model.encode(chunks)

# embeddings = np.array(
#     embeddings,
#     dtype=np.float32
# )

# # -------------------------
# # FAISS INDEX
# # -------------------------
# dimension = embeddings.shape[1]

# index = faiss.IndexFlatL2(dimension)

# index.add(embeddings)

# print("FAISS Ready")


# # -------------------------
# # CHAT LOOP
# # -------------------------
# while True:

#     question = input("\nAsk Question: ")

#     if question.lower() == "exit":
#         break

#     query_embedding = model.encode(
#         [question]
#     )

#     query_embedding = np.array(
#         query_embedding,
#         dtype=np.float32
#     )

#     D, I = index.search(
#         query_embedding,
#         k=3
#     )

#     context = ""

#     for idx in I[0]:
#         context += chunks[idx] + "\n"

#     prompt = f"""
#     You are a resume assistant.

#     Resume Content:
#     {context}

#     Question:
#     {question}

#     Answer based only on resume.
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

#     print("\nAnswer:")
#     print(
#         response["message"]["content"]
#     )