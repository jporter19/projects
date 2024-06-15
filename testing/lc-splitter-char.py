#%%
# %pip install --upgrade --quiet langchain-text-splitters tiktoken
from langchain_text_splitters import CharacterTextSplitter
from pprint import pprint

# This is a long document we can split up.
with open("b:/code/data/mfm_pod_alex.txt") as f:
    essay = f.read()

from langchain_text_splitters import CharacterTextSplitter

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

texts = text_splitter.create_documents([essay])
print(texts[0])
# %% -------------- I'm not sure what this is doing
# metadatas = [{"document": 1}, {"document": 2}]
# documents = text_splitter.create_documents(
#    [essay, essay], metadatas=metadatas)
# print(len(documents))
# print(documents[175])

# %%
