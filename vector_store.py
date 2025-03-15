from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from embedding import doc_embeddings

client = QdrantClient(":memory:")

client.create_collection(
    collection_name="jobs",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="jobs",
    embedding=doc_embeddings,
)