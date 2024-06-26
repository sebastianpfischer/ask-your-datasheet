from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.chroma import Chroma

# Retrieve the embeddings from the Chroma vector store
embeddings = OllamaEmbeddings(model="mistral")
vector_db = Chroma(
    "micro-processor-datasheet", embeddings, persist_directory="./chroma"
)

query = "which ARM is it the datasheet from?"
result = vector_db.similarity_search(query)
print(result[0].page_content)
