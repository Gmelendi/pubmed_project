# encoding=utf-8

from haystack.document_store import ElasticsearchDocumentStore
from haystack.retriever import DensePassageRetriever
from haystack.reader import TransformersReader
from haystack import Pipeline


def get_ElasticSearchDocumentStore():

    return ElasticsearchDocumentStore(
        host='localhost', 
        port=9200, 
        similarity="dot_product")

def get_DensePassageRetriever(document_store):

    return DensePassageRetriever(
        document_store=document_store,
        query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
        passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base"
    )

def get_Reader():
    return TransformersReader("deepset/roberta-base-squad2", use_gpu=-1)

def get_Pipeline(retriever=get_DensePassageRetriever(get_ElasticSearchDocumentStore()), reader=get_Reader()):

    p = Pipeline()
    p.add_node(component=retriever, name="ESRetriever1", inputs=["Query"])
    p.add_node(component=reader, name="QAReader", inputs=["ESRetriever1"])
    
    # res = p.run(query="What did Einstein work on?", top_k_retriever=1)
    return p