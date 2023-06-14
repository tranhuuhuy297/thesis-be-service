import pinecone
from sentence_transformers import SentenceTransformer

# initialize sentence transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

PINECONE_API_KEY = '10a1b9c4-42b2-41fe-a91b-ab9c6f4a0a8a'
PINECONE_ENV = 'us-west4-gcp'
PINECONE_INDEX = 'thesis'

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)


class Pinecone:
    def __init__(self, index=PINECONE_INDEX, namespace='crawl_prompt'):
        self.index = pinecone.Index(index)
        self.namespace = namespace

    def upsert(self, list_id, list_text, list_metadata):
        embeddings = model.encode(list_text)
        vectors = list(zip(list_id, [embed.tolist() for embed in embeddings], list_metadata))
        num_upsert = self.index.upsert(vectors, namespace=self.namespace)

        return num_upsert

    def query(self, query, top_k=100):
        embed = model.encode(query).tolist()
        return self.index.query(embed, top_k=top_k, include_metadata=True, namespace=self.namespace)

    def delete(self, list_id=[], delete_all=False):
        num_delete = self.index.delete(list_id, deleteAll=delete_all, namespace=self.namespace)
        return num_delete
