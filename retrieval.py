# encoding=utf-8

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def retrieval_stage(query, items, k=100):

    df = pd.DataFrame(
        columns=['query', 'items'], 
        data=[
            pd.Series([query]*len(items)),
            pd.Series(items)
        ])

    model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
    q_embeddings = model.encode(query)

    items_embeddings = model.encode(items)

    df['similarity'] = cosine_similarity(q_embeddings, items_embeddings)

    return df
