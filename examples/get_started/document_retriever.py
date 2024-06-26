import os
from pathlib import Path

from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma

readme_path = Path(__file__).parent.parent.parent / "README.md"
pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"

# Loading
loaders = [TextLoader(str(readme_path)), TextLoader(str(pyproject_path))]
docs = []
for loader in loaders:
    docs.extend(loader.load())
# print(docs)

# This text splitter is used to create the child documents
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

# Embedding
embeddings_model = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.environ["HUGGINGFACEHUB_API_TOKEN"],
    model_name="sentence-transformers/all-MiniLM-l6-v2",
)

# The vectorstore to use to index the child chunks
vectorstore = Chroma(
    collection_name="full_documents", embedding_function=embeddings_model
)
# The storage layer for the parent documents
store = InMemoryStore()
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
)

retriever.add_documents(docs, ids=None)

list(store.yield_keys())

sub_docs = vectorstore.similarity_search("classifiers")
print(sub_docs[0].page_content)
retrieved_docs = retriever.get_relevant_documents("classifiers")
print(retrieved_docs[0].page_content[:100])
