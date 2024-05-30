import pinecone
from sentence_transformers import SentenceTransformer
from util.logger_util import logger
from util.const_util import PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX, MODEL_NAME

# initialize sentence transformer model
model = SentenceTransformer(MODEL_NAME)

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)


class Pinecone:
    def __init__(self, index=PINECONE_INDEX, namespace='crawl_prompt'):
        self.pinecone_client = pinecone
        self.index = self.pinecone_client.Index(index)
        self.namespace = namespace

    def upsert(self, list_id, list_text, list_metadata, namespace=None):
        logger.info(f'upsert {list_metadata}')
        embeddings = model.encode(list_text)
        vectors = list(zip(list_id, [embed.tolist() for embed in embeddings], list_metadata))
        num_upsert = self.index.upsert(vectors=vectors, namespace=namespace or self.namespace)

        return num_upsert

    def query(self, query, top_k=100, namespace=None):
        embed = model.encode(query).tolist()
        result = self.index.query(embed, top_k=top_k, include_metadata=True, namespace=namespace or self.namespace)
        return result.to_dict()['matches']

    def delete(self, list_id=[], delete_all=False, namespace=None):
        num_delete = self.index.delete(list_id, deleteAll=delete_all, namespace=namespace or self.namespace)
        return num_delete
