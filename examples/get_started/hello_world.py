import os

from langchain.llms.huggingface_hub import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, StrOutputParser

# Get LLM
llm = HuggingFaceHub(
    repo_id="google/flan-t5-xxl",
    model_kwargs={"temperature": 0.2, "max_new_tokens": 200},
)

# Create a prompt
template = """
Just tell me what is in the ""
For example, for "Hello World", you would answer "Hello World".

"{content}"
"""
my_prompt = PromptTemplate(template=template, input_variables=["content"])

# Create llm chain
my_chain = my_prompt | llm | StrOutputParser()

# Get the responses
llm_response = my_chain.invoke({"content": "colorful socks"})


if __name__ == "__main__":
    pass
    print(llm_response)
