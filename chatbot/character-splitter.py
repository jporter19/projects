
#%%
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter

# %% LangChain TextSplitter
# word seperators \n\n,\n,.," ",""
# chunk size 1000, model handles 256 words and average english token size is 4 per word, so (4*250)= 1000
def splitting(input_texts):
    char_splitter = RecursiveCharacterTextSplitter(
        separators= ["\n\n", "\n", ". ", " ", ""],
        chunk_size=1000,
        chunk_overlap=0.2
        )
    # we're joining individual lines based on double-line break
    texts_char_splitted = char_splitter.split_text('\n\n'.join(input_texts))
    print(f"Number of chunks: {len(texts_char_splitted)}")
    ## %%
    # create a token splitter object using default model
    token_splitter = SentenceTransformersTokenTextSplitter(
        chunk_overlap=0.2,
        tokens_per_chunk=256
        )
    #create an empty list
    texts_token_splitted = []
    # for each text  in texts_Char_splitted call token splitter put tokens in list
    # note some texts are getting errors
    for text in texts_char_splitted:
        try:
            texts_token_splitted.extend(token_splitter.split_text(text))
        except:
            print(f"Error in text: {text}")
            continue
    # about 100 chunks lost due to error or removal
    print(f"Number of chunks: {len(texts_token_splitted)}")

    # %%
    # show the first chunk
    pprint(texts_token_splitted[0])

    # %% Create a reference to a new Vector Database and create a collection in db called ipcc
    chroma_client = chromadb.PersistentClient(path="db")
    chroma_collection = chroma_client.get_or_create_collection(newcol)

    # %% Add Documents
    metadatas=[{"source":pdf_name} for i in range(len(texts_token_splitted))]
    ids = [str(uuid.uuid4()) for i in range(len(texts_token_splitted))]
    chroma_collection.add(
        ids=ids,
        documents=texts_token_splitted,
        metadatas=metadatas
        )
    # %% query DB
    query = "how many times did you talk to mary?"
    res = chroma_collection.query(query_texts=[query], n_results=5)

# %%
#--------------------- New Version -------------------------------
#%% packages
import re
import pandas as pd
import seaborn as sns
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from pprint import pprint
#-----------------------------------------

# %% max_length
def max_word_count(txt_list:list):
    max_length = 0
    for txt in txt_list:
        word_count = len(re.findall(r'\w+', txt))
        if word_count > max_length:
            max_length = word_count
    return f"Max Word Count: {max_length} words"

# %% Sentence splitter
# chroma default sentence model "all-MiniLM-L6-v2"
# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
# max input length: 256 characters
model_max_chunk_length = 256
token_splitter = SentenceTransformersTokenTextSplitter(
    tokens_per_chunk=model_max_chunk_length,
    model_name="all-MiniLM-L6-v2",
    chunk_overlap=0
)

# %% Data Import
text_path = "../data/movies.csv"
# create a dataframe with everything in csv
df_movies_raw = pd.read_csv(text_path, parse_dates=['release_date'])
# show the first two rows
df_movies_raw.head(2)
# len(df_movies_raw)

#%% filter movies for missing title or overwiew
#selected_cols = ['id', 'title', 'overview', 'vote_average', 'release_date']
# df_movie_raw is a pandas dataframe with all data
# df_movie_filt is a pandas dataframe with selected rows with blank rows dropped
# df_movies_filt = df_movies_raw[selected_cols].dropna()
df_movies_filt = df_movies_raw.dropna(subset=['title','overview'])
#shoe that only selected columns are in head
len(df_movies_filt)
df_movies_filt.head(2)

#%%
# filter for unique ids, dropping rows with duplicate IDs
df_movies_filt = df_movies_filt.drop_duplicates(subset=['id'])

# filter for movies after 01.01.2023
# df_movies_filt = df_movies_filt[df_movies_filt['release_date'] > '2023-01-01']
df_movies_filt.shape
#%%


# %%
max_word_count(df_movies_filt['overview'])

#%% Word Distribution
descriptions_len = []
for txt in df_movies_filt.loc[:, "overview"]:
    descriptions_len.append(len(re.findall(r'\w+', txt)))

#%% visualize token distribution
sns.histplot(descriptions_len, bins=100)

# %%
embedding_fn = SentenceTransformerEmbeddingFunction()


#%%
# chroma_collection.add(documents=documents, ids=ids, metadatas=metadatas)
batch_size = 5000
for i in range(0,len(ids),batch_size):
    chroma_collection.add(ids=ids[i:i+batch_size], 
    documents=documents[i:i+batch_size],metadatas=metadatas[i:i+batch_size])
    print(i)

#%% count of documents in collection
len(chroma_collection.get()['ids'])

# %% Save the chroma collection
# %% Run a Query
def get_title_by_description(query_text:str):
    n_results = 10
    res = chroma_collection.query(query_texts=[query_text], n_results=n_results)
    for i in range(n_results):
        pprint(f"Title: {res['metadatas'][0][i]['source']} \n")
        pprint(f"Description: {res['documents'][0][i]} \n")
        pprint("-------------------------------------------------")

#%% Run a Query
get_title_by_description(query_text="live action talking animals")

# %%
