import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from groq import Groq

load_dotenv()

def load_and_chunk(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)
    print(f"Split PDF into {len(chunks)} chunks")
    return chunks

def build_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma.db"
    )

    print("Vectorstore built and saved!")
    return vectorstore

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory="./chroma.db",
        embedding_function=embeddings
    )
    return vectorstore

def retrieve_context(vectorstore, question, k=4):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])
    return context

def ask_groq(question, context):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are a helpful assistant. Use ONLY the context below to answer 
the question. If the answer isn't in the context, say "I don't know based on 
the provided documents."

Context:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def answer_question(question, pdf_path=None):
    if pdf_path:
        chunks = load_and_chunk_pdf(pdf_path)
        vectorstore = build_vectorstore(chunks)
    else:
        vectorstore = load_vectorstore()

    context = retrieve_context(vectorstore, question)
    answer = ask_groq(question, context)
    return answer