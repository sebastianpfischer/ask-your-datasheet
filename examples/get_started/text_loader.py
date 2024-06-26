import os
from pathlib import Path

from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.vectorstores.chroma import Chroma

readme_path = Path(__file__).parent.parent.parent / "README.md"

# Loading
loader = TextLoader(readme_path)
loaded_readme = loader.load()

# print(loaded_readme)

# Transforming
text_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "Header 1"),
        ("##", "Header 2"),
    ]
)

transformed_readme = text_splitter.split_text(loaded_readme[0].page_content)
# transformed_readme2 = text_splitter.split_documents(loaded_readme)

# for text in transformed_readme:
#    print(type(text))
#    print(text)

# Embedding
embeddings_model = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.environ["HUGGINGFACEHUB_API_TOKEN"],
    model_name="sentence-transformers/all-MiniLM-l6-v2",
)


embeddings = embeddings_model.embed_documents([str(doc) for doc in transformed_readme])

# Create a vector store
db = Chroma.from_documents(transformed_readme, embeddings_model)

# Do a search for similar content with a query:
query = "Warning?"
docs = db.similarity_search(query)
print(docs[0].page_content)

# Do a search for similar content with a embedding query:
embedding_vector = embeddings_model.embed_query("Warning?")
docs = db.similarity_search_by_vector(embedding_vector)
print(docs[0].page_content)
