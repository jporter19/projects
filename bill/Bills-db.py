#%%
import os
import chromadb
from openai import OpenAI
from pprint import pprint
import re
from tqdm import tqdm
from chromadb.config import Settings
client = chromadb.Client(Settings(anonymized_telemetry=False))

# pyinstaller --onefile --paths venv/lib/site-packages --add-data "db/*;db" Bills-db.py

#%% -----------------------  Get Collection ---------------------
# Create a reference to a new Vector Database and create a collection in db called ipcc

user_input = input("please enter a question")
chroma_db = chromadb.PersistentClient(path="db")  # open db
chroma_collection = chroma_db.get_collection("bluemetal") # open collection
# print(chroma_db.list_collections()) # print all collections in database

query = user_input
res = chroma_collection.query(query_texts=[query], 
    n_results=3,
    include=["documents"])

user_content = query
system_content = "Acting as a professional editor, summarize a response for the using only information from assistant. If there are multiple points then please bullet each point"
assist_content = str(res["documents"][0])


#%#%---------------- Initialize OpenAI Client ------------------------------------
import os
from openai import OpenAI

client = OpenAI(
    # This gets my OpenAI "OPENAI_API_KEY" environment variable for Windows
    # OPENAI_API_KEY is the default, so "client=OpenAI()" would work
    api_key=os.environ.get("OPENAI_API_KEY")
)
def print_response(response):
    try:
        print(response.choices[0].message.content)
    except TypeError:
        print("Error: Unable to retrieve response. Please check your completion object.")

completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_content
        },
        {
            "role": "system",
            "content": system_content
        },
        {
            "role": "assistant",
            "content": assist_content
        }
    ],
    model="gpt-3.5-turbo"   # There are other models, but this one is good and affordable
)
print_response(completion)


# %%
