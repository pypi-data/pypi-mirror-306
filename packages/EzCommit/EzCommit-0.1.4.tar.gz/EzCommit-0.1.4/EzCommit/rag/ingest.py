from .utils import get_commit_diff
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language
from langchain_text_splitters import RecursiveCharacterTextSplitter
from constants import (
    COMMIT_COLLECTION
)

class Ingest:
    def __init__(self, client, llm_client, repo, config):
        self.client = client 
        self.llm_client = llm_client
        self.repo = repo
        self.config = config
    
    def update_database(self):
        collection = self.client.get_or_create_collection(COMMIT_COLLECTION)
        for commit in self.repo.iter_commits():
            existing_commit = collection.get(ids=[commit.hexsha])
            if existing_commit['ids']:
                continue

            commit_diff = get_commit_diff(commit, self.config.repo_path, self.llm_client)
            print(f"Processing commit {commit.hexsha}")

            collection.add(
                ids=[commit.hexsha],
                documents=[commit_diff],
                metadatas=[{"author": commit.author.name, "date": commit.committed_datetime.isoformat()}]
            )
        # Load
        loader = GenericLoader.from_filesystem(
            self.config.repo_path,
            glob="**/*",
            suffixes=[".py", ".ipynb"],
            exclude=["**/non-utf8-encoding.py"],
            parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
        )
        documents = loader.load()
        python_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
        )
        texts = python_splitter.split_documents(documents)
        for i in range(len(texts)):
            existing_code = collection.get(ids=[f"code_{i}"]) 
            if existing_code['ids']:
                continue
            
            collection.add(
                ids=[f"code_{i}"], 
                documents=[texts[i].page_content], 
                metadatas=[texts[i].metadata]
            )
