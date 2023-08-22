import os
from typing import List
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup

from opencopilot import OpenCopilot

load_dotenv()

copilot = OpenCopilot(
    prompt_file="prompts/prompt_template.txt",
    copilot_name="llm",
    auth_type=None,
    helicone_api_key=os.getenv("HELICONE_API_KEY")
)
copilot.add_local_files_dir("data")

@copilot.data_loader
def load_opencopilot_docs() -> List[Document]:
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=2000,
        model_name="gpt-4",
        separator=" ",
        disallowed_special=(),
    )
    loader = RecursiveUrlLoader(url="https://docs.opencopilot.dev/", extractor=lambda x: Soup(x, "html.parser").text)
    documents = loader.load()
    document_chunks = []
    for document in documents:
        for chunk in text_splitter.split_text(document.page_content):
            document_chunks.append(Document(page_content=chunk, metadata=document.metadata))
    return document_chunks

copilot()
