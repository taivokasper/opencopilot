import os
from typing import List
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup

from opencopilot import OpenCopilot

load_dotenv()

copilot = OpenCopilot(
    copilot_name="llm",
    auth_type=None,
    helicone_api_key=os.getenv("HELICONE_API_KEY")
)

copilot.add_prompt("prompts/prompt_template.txt")
copilot.add_local_files_dir("data")

@copilot.data_loader
def load_opencopilot_docs() -> List[Document]:
    loader = RecursiveUrlLoader(url="https://docs.opencopilot.dev/", extractor=lambda x: Soup(x, "html.parser").text)
    documents = loader.load()
    return documents

copilot()