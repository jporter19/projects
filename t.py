#%%
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

# Load HTML
loader = AsyncChromiumLoader(["https://www.wsj.com"])
html = loader.load()
print(html)
# %%
