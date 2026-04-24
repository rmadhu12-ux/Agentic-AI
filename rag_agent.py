import os
import shutil
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. CONFIGURATION & SECURITY
# Replace with your actual key or use os.getenv("GOOGLE_API_KEY") if using .env
os.environ["GOOGLE_API_KEY"] = "AIzaSyDJt297G2-qlqZyKOP8p3mEhcpCxq2So0g"
DB_PATH = "./chroma_db"

# Cleanup: Ensures no corrupted data from previous failed runs remains
if os.path.exists(DB_PATH):
    shutil.rmtree(DB_PATH)

# 2. LOAD DATA
print("--- Step 1: Loading Data ---")
if not os.path.exists("wonders.txt"):
    with open("wonders.txt", "w", encoding="utf-8") as f:
        f.write("Machu Picchu is a 15th-century Inca citadel located in the Eastern Cordillera of southern Peru on a 2,430-meter mountain ridge. It is located in the Machupicchu District within Urubamba Province.")
    print("Created a sample wonders.txt file.")

loader = TextLoader("wonders.txt", encoding="utf-8")
docs = loader.load()

# 3. TEXT SPLITTING & SANITIZATION
print("--- Step 2: Splitting Text ---")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
raw_splits = text_splitter.split_documents(docs)

# Remove empty chunks which cause the IndexError in 2026 Google API
splits = [doc for doc in raw_splits if doc.page_content.strip()]
print(f"Total valid chunks to index: {len(splits)}")

# 4. VECTOR DATABASE (MANUAL ADDITION FOR STABILITY)
print("--- Step 3: Creating Vector Database ---")
embeddings_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    task_type="retrieval_document"
)

# Initialize an empty database
vectorstore = Chroma(
    embedding_function=embeddings_model,
    persist_directory=DB_PATH
)

# Add documents one-by-one to avoid batch-count IndexErrors
for i, split in enumerate(splits):
    vectorstore.add_documents([split])
    print(f"  Indexed chunk {i+1}/{len(splits)}")

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 5. LLM SETUP (GEMINI 3.1)
print("--- Step 4: Initializing Gemini LLM ---")
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0)

system_prompt = (
    "You are a helpful assistant. Use the following context to answer the question. "
    "If you don't know, say you don't know. Keep answers concise.\n\n"
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 6. RAG CHAIN CONSTRUCTION
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# 7. EXECUTION
question = input("Question : ")
print(f"\nQuestion: {question}")

try:
    response = rag_chain.invoke({"input": question})
    print("-" * 30)
    print(f"Answer: {response['answer']}")
    print("-" * 30)
except Exception as e:
    print(f"An error occurred during generation: {e}")