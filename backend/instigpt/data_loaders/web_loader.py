from chromadb.api import ClientAPI
from langchain_core.embeddings import Embeddings
from langchain.document_loaders import WebBaseLoader
from requests.exceptions import TooManyRedirects
import pandas as pd
import numpy as np
import requests
import PyPDF2
import shutil
import os
import time

from instigpt import config
from . import pdf


def load_pdf_from_urls_list(
    client: ClientAPI,
    embeddings: Embeddings,
    document_name: str,
    url_list: list,
) -> int:
    """Extracts pdfs from links in csv, chunks them and stores the chunks in the
    database along with its embeddings.

    returns: int: number of chunks stored in the database
    """
    pdfs = url_list
    os.mkdir("generated_pdfs")
    n_docs = 0
    for i in range(len(pdfs)):
        if len(pdfs) == 0:
            break
        response = requests.get(pdfs[i])
        with open(f'generated_pdfs/{document_name}PDF{i}.pdf', 'wb') as f:
            f.write(response.content)
            file_path = f'generated_pdfs/{document_name}PDF{i}.pdf'
            try:
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    num_pages = len(pdf_reader.pages)
                if num_pages == 0:
                    continue
            except PyPDF2.errors.PdfReadError as e:
                print(f"PdfReadError: Encountered a problem with '{file_path}': {e}")
                print(f"Skipping '{file_path}' due to the PdfReadError.")
                continue
            n_docs += pdf.load_pdf_data(client=client, embeddings = embeddings, document_name = f"{document_name}PDF{i}_", data_path = file_path)
    shutil.rmtree("generated_pdfs")


    return n_docs

def load_html_from_urls_list(
    client: ClientAPI,
    embeddings: Embeddings,
    document_name: str,
    url_list: list,
) -> int: 
    docs = url_list
    batches = np.array_split(docs, len(docs) // 200)  # Splitting into batches of size 200
    batch_num = 0
    for batch in batches:
        batch_num += 1
        html_parsed = []
        for url in batch:
            try:
                loader = WebBaseLoader(url ,default_parser= 'lxml', encoding='utf-8')
                doc = loader.load()
                html_parsed += doc
            except TooManyRedirects:
                print("Too many redirects, waiting 10 seconds")
                time.sleep(5)
        ids = [f"{document_name}-{batch_num}-{i}" for i in range(len(html_parsed))]
        metadatas = [{"source": document_name} for _ in range(len(html_parsed))]
        coll = client.get_or_create_collection(config.COLLECTION_NAME)
        # NOTE: The embeddings are automatically computed using the emdbedding function passed to the collection
        coll.add(
            documents=html_parsed,
            embeddings=embeddings.embed_documents(html_parsed),  # type: ignore
            metadatas=list(metadatas),
            ids=ids,
        )
    return len(docs)
            
def load_web_urls_in_csv_data(
    client: ClientAPI,
    embeddings: Embeddings,
    document_name: str,
    data_path: str,
) -> int: 
    df = pd.read_csv(data_path)
    docs = []
    pdfs = []
    for url in df.iloc[:, 0]:
        if url[-3:] == "jpg" or url[-3:] == "png" or url[-4:] == "jpeg":
            continue
        elif url[-3:] == "pdf":
            pdfs.append(url)
        else:
            docs.append(url)
    n_pdfs = load_pdf_from_urls_list(client=client, embeddings=embeddings,document_name=document_name, url_list=pdfs)
    n_html = load_html_from_urls_list(client=client, embeddings=embeddings,document_name=document_name, url_list=docs)
    
    return n_pdfs + n_html