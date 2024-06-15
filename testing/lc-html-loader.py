#%%
from langchain_community.document_loaders import UnstructuredHTMLLoader

loader = UnstructuredHTMLLoader("file.html")  # not a website
data = loader.load()
data
# %%
