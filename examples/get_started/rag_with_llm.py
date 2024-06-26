from langchain import hub
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Retrieve the embeddings from the Chroma vector store
embeddings = OllamaEmbeddings(model="mistral")
vector_db = Chroma(
    "micro-processor-datasheet", embeddings, persist_directory="./chroma"
)
retriever = vector_db.as_retriever()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Get LLM
llm_ollama = Ollama(model="mistral")

# Get steps to build the chain
prompt = hub.pull("rlm/rag-prompt")


if __name__ == "__main__":
    # Question to ask
    query = "which ARM is the datasheet for?"

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm_ollama
        | StrOutputParser()
    )

    result = rag_chain.invoke(query)
    print(result)
    print("--------------------------------")
    result = rag_chain.invoke("How to configure the interruption routine?")
    print(result)
