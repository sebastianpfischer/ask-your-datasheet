from pathlib import Path
from time import sleep

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.chroma import Chroma

# Load a PDF document
loader = PyPDFLoader(Path(__file__).parent / "dm00037051.pdf", extract_images=False)
documents = loader.load()

# Split the text into chunks
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# Embed the text chunks
embeddings = OllamaEmbeddings(model="mistral")

# Create a vector store
vector_db = Chroma(
    "micro-processor-datasheet", embeddings, persist_directory="./chroma"
)
vector_db.add_documents(docs)

query = "which ARM is it the datasheet from?"
result = vector_db.similarity_search(query)
print(result[0].page_content)
