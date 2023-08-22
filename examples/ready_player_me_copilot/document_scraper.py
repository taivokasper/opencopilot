import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Callable
from typing import List

from langchain.schema import Document

import blog_loader
import gitbook_loader
import url_loader

LOADERS_MAP = {
    "gitbook": gitbook_loader.execute,
    "url": url_loader.execute,
    "blog": blog_loader.execute,
}


class SourceType(Enum):
    GITBOOK = "gitbook"
    URL = "url"
    BLOG = "blog"


@dataclass
class DataLoader:
    source_type: SourceType
    sources: List[str]
    destination_file: str  # myfile.json


def execute(data_loaders: List[DataLoader]):
    for data_loader in data_loaders:
        if loader := LOADERS_MAP.get(data_loader.source_type.value):
            _scrape(
                file_dump_path=data_loader.destination_file,
                loader_function=loader,
                urls=data_loader.sources,
            )


def _scrape(
        file_dump_path: str,
        loader_function: Callable[[List[str]], List[Document]],
        urls: List[str],
) -> None:
    if not os.path.exists(file_dump_path):
        scraped_documents = loader_function(urls)

        json_docs = [d.json() for d in scraped_documents]
        formatted_docs = [json.loads(d) for d in json_docs]

        file_dump_dir = os.path.dirname(file_dump_path)
        if file_dump_dir:
            os.makedirs(file_dump_dir, exist_ok=True)
        with open(file_dump_path, "w") as f:
            f.write(json.dumps(formatted_docs, indent=4))
