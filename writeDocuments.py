# encoding=utf-8
import os
import json

from haystack import retriever
from connection import get_ElasticSearchDocumentStore, get_DensePassageRetriever

def main():

    # list all json documents to write
    DATA_DIR = 'data'
    docs = [os.path.join(DATA_DIR, file_) for file_ in os.listdir(DATA_DIR) if 'json' in file_]

    # Instanciate a DocumentStore ElasticSearch Database
    document_store = get_ElasticSearchDocumentStore()
    # delete all documents, if any
    document_store.delete_all_documents()

    for doc in docs:

        # read data file
        with open(doc, 'r') as f:
            doc_data = json.load(f)

        # save to document store
        document_store.write_documents(doc_data)

    # instanciate Retriever
    retriever = get_DensePassageRetriever(document_store)
    # generate embeddings for each doc
    document_store.update_embeddings(retriever)        

if __name__ == '__main__':

    main()