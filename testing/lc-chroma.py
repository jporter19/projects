#%%
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,)
from langchain_text_splitters import CharacterTextSplitter

# --------------   Load Text Data  ----------------
# load the document and split it into chunks
loader = TextLoader("b:/code/data/mfm_pod_alex.txt")
documents = loader.load()

# --------------   Chunk data  ----------------
# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
# ----------  Create embedding function  ----------
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# -----------  put docs & embeddings in vector store ------------
# This creates an "in-memory chroma db" this is not on disk
db = Chroma.from_documents(docs, embedding_function)
# ----------------  Run query to confirm results  -----------------
query = "who grows up playing sports"
docs = db.similarity_search(query)
# print results
print(docs[0].page_content)

#%% ---------------  Chroma.from_documents -----------------------
# This creates a persistent database using documents in memory
db2 = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")
docs=[]  # clear docs
docs = db2.similarity_search(query) # run same query from persistent db
print(docs[0].page_content)    # same result

#%%  ----------- initialize db3 to read from existing chroma DB ----------
# load from disk
db3 = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
docs = db3.similarity_search(query)
print(docs[0].page_content)

#%%

import chromadb

persistent_client = chromadb.PersistentClient()
collection = persistent_client.get_or_create_collection("collection_name")
collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])

langchain_chroma = Chroma(
    client=persistent_client,
    collection_name="collection_name",
    embedding_function=embedding_function,
)

print("There are", langchain_chroma._collection.count(), "in the collection")

# %%
retriever = db.as_retriever(search_type="mmr")
retriever.invoke(query)[0]

#%%
# create simple ids
ids = [str(i) for i in range(1, len(docs) + 1)]

# add data new db
example_db = Chroma.from_documents(docs, embedding_function, ids=ids)
docs = example_db.similarity_search(query)
print(docs[0].metadata)

#%%
# update the metadata for a document
docs[0].metadata = {
    "source": "../../data/mfm_pod_alex.txt",
    "new_value": "hello world",
}
example_db.update_document(ids[0], docs[0])
print(example_db._collection.get(ids=[ids[0]]))

# delete the last document
print("count before", example_db._collection.count())
example_db._collection.delete(ids=[ids[-1]])
print("count after", example_db._collection.count())

# %%
# filter collection for updated source
# example_db.get(where={"source": "some_other_source"})