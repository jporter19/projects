#%%
# Make the display a bit wider
# from IPython.display import display, HTML
# display(HTML("<style>.container { width:90% !important; }</style>"))

# LangChain basics
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import create_extraction_chain

# Vector Store and retrievals
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma, Pinecone
import pinecone

# Chat Prompt templates for dynamic values
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

# Supporting libraries
import os
from dotenv import load_dotenv

load_dotenv()


# Creating two versions of the model so I can swap between gpt3.5 and gpt4
llm3 = ChatOpenAI(temperature=0,
                  openai_api_key=os.getenv('OPENAI_API_KEY', 'YourAPIKeyIfNotSet'),
                  model_name="gpt-3.5-turbo-0613",
                  request_timeout = 180
                )

llm4 = ChatOpenAI(temperature=0,
                  openai_api_key=os.getenv('OPENAI_API_KEY', 'YourAPIKeyIfNotSet'),
                  model_name="gpt-4-0613",
                  request_timeout = 180
                 )


# I put three prepared transcripts
transcript_paths = [
    '../data//mfm_pod_steph.txt',
    '../data/mfm_pod_alex.txt',
    '../data/mfm_pod_rob.txt'
]

with open('../data/mfm_pod_steph.txt') as file:
    transcript = file.read()
print(transcript[:280])

# Load up your text splitter
text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " "], chunk_size=10000, chunk_overlap=2200)

# I'm only doing the first 23250 characters. This to save on costs. When you're doing your exercise you can remove this to let all the data through
transcript_subsection_characters = 23250
docs = text_splitter.create_documents([transcript[:transcript_subsection_characters]])
print (f"You have {len(docs)} docs. First doc is {llm3.get_num_tokens(docs[0].page_content)} tokens")
# %%

template="""
You are a helpful assistant that helps retrieve topics talked about in a podcast transcript
- Your goal is to extract the topic names and brief 1-sentence description of the topic
- Topics include:
  - Themes
  - Business Ideas
  - Interesting Stories
  - Money making businesses
  - Quick stories about people
  - Mental Frameworks
  - Stories about an industry
  - Analogies mentioned
  - Advice or words of caution
  - Pieces of news or current events
- Provide a brief description of the topics after the topic name. Example: 'Topic: Brief Description'
- Use the same words and terminology that is said in the podcast
- Do not respond with anything outside of the podcast. If you don't see any topics, say, 'No Topics'
- Do not respond with numbers, just bullet points
- Do not include anything about 'Marketing Against the Grain'
- Only pull topics from the transcript. Do not use the examples
- Make your titles descriptive but concise. Example: 'Shaan's Experience at Twitch' should be 'Shaan's Interesting Projects At Twitch'
- A topic should be substantial, more than just a one-off comment

% START OF EXAMPLES
 - Sam’s Elisabeth Murdoch Story: Sam got a call from Elizabeth Murdoch when he had just launched The Hustle. She wanted to generate video content.
 - Shaan’s Rupert Murdoch Story: When Shaan was running Blab he was invited to an event organized by Rupert Murdoch during CES in Las Vegas.
 - Revenge Against The Spam Calls: A couple of businesses focused on protecting consumers: RoboCall, TrueCaller, DoNotPay, FitIt
 - Wildcard CEOs vs. Prudent CEOs: However, Munger likes to surround himself with prudent CEO’s and says he would never hire Musk.
 - Chess Business: Priyav, a college student, expressed his doubts on the MFM Facebook group about his Chess training business, mychesstutor.com, making $12.5K MRR with 90 enrolled.
 - Restaurant Refiller: An MFM Facebook group member commented on how they pay AirMark $1,000/month for toilet paper and toilet cover refills for their restaurant. Shaan sees an opportunity here for anyone wanting to compete against AirMark.
 - Collecting: Shaan shared an idea to build a mobile only marketplace for a collectors’ category; similar to what StockX does for premium sneakers.
% END OF EXAMPLES
"""
system_message_prompt_map = SystemMessagePromptTemplate.from_template(template)

human_template="Transcript: {text}" # Simply just pass the text as a human message
human_message_prompt_map = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt_map = ChatPromptTemplate.from_messages(messages=[system_message_prompt_map, human_message_prompt_map])

template="""
You are a helpful assistant that helps retrieve topics talked about in a podcast transcript
- You will be given a series of bullet topics of topics vound
- Your goal is to exract the topic names and brief 1-sentence description of the topic
- Deduplicate any bullet points you see
- Only pull topics from the transcript. Do not use the examples

% START OF EXAMPLES
 - Sam’s Elisabeth Murdoch Story: Sam got a call from Elizabeth Murdoch when he had just launched The Hustle. She wanted to generate video content.
 - Shaan’s Rupert Murdoch Story: When Shaan was running Blab he was invited to an event organized by Rupert Murdoch during CES in Las Vegas.
% END OF EXAMPLES
"""
system_message_prompt_map = SystemMessagePromptTemplate.from_template(template)

human_template="Transcript: {text}" # Simply just pass the text as a human message
human_message_prompt_map = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt_combine = ChatPromptTemplate.from_messages(messages=[system_message_prompt_map, human_message_prompt_map])



chain = load_summarize_chain(llm4,
                             chain_type="map_reduce",
                             map_prompt=chat_prompt_map,
                             combine_prompt=chat_prompt_combine,
#                              verbose=True
                            )
topics_found = chain.run({"input_documents": docs})
print (topics_found)

# %%
schema = {
    "properties": {
        # The title of the topic
        "topic_name": {
            "type": "string",
            "description" : "The title of the topic listed"
        },
        # The description
        "description": {
            "type": "string",
            "description" : "The description of the topic listed"
        },
        "tag": {
            "type": "string",
            "description" : "The type of content being described",
            "enum" : ['Business Models', 'Life Advice', 'Health & Wellness', 'Stories']
        }
    },
    "required": ["topic", "description"],
}

chain = create_extraction_chain(schema, llm3)
topics_structured = chain.run(topics_found)
topics_structured
# %%

text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=800)

docs = text_splitter.create_documents([transcript[:transcript_subsection_characters]])

print (f"You have {len(docs)} docs. First doc is {llm3.get_num_tokens(docs[0].page_content)} tokens")

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))

# load it into Chroma
docsearch = Chroma.from_documents(docs, embeddings)

# The system instructions. Notice the 'context' placeholder down below. This is where our relevant docs will go.
# The 'question' in the human message below won't be a question per se, but rather a topic we want to get relevant information on
system_template = """
You will be given text from a podcast transcript which contains many topics.
You goal is to write a summary (5 sentences or less) about a topic the user chooses
Do not respond with information that isn't relevant to the topic that the user gives you
----------------
{context}"""

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]

# This will pull the two messages together and get them ready to be sent to the LLM through the retriever
CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)
# I'm using gpt4 for the increased reasoning power.
# I'm also setting k=4 so the number of relevant docs we get back is 4. This parameter should be tuned to your use case
qa = RetrievalQA.from_chain_type(llm=llm4,
                                 chain_type="stuff",
                                 retriever=docsearch.as_retriever(k=4),
                                 chain_type_kwargs = {
#                                      'verbose': True,
                                     'prompt': CHAT_PROMPT
                                 })

# Only doing the first 3 for conciseness 
for topic in topics_structured[:5]:
    query = f"""
        {topic['topic_name']}: {topic['description']}
    """

    expanded_topic = qa.run(query)

    print(f"{topic['topic_name']}: {topic['description']}")
    print(expanded_topic)
    print ("\n\n")

# %%
system_template = """
What is the first timestamp when the speakers started talking about a topic the user gives?
Only respond with the timestamp, nothing else. Example: 0:18:24
----------------
{context}"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]
CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)
qa = RetrievalQA.from_chain_type(llm=llm4,
                                 chain_type="stuff",
                                 retriever=docsearch.as_retriever(k=4),
                                 chain_type_kwargs = {
#                                      'verbose': True,
                                     'prompt': CHAT_PROMPT
                                 })
# Holder for our topic timestamps
topic_timestamps = []

for topic in topics_structured:

    query = f"{topic['topic_name']} - {topic['description']}"
    timestamp = qa.run(query)
    
    topic_timestamps.append(f"{timestamp} - {topic['topic_name']}")
# %%
print ("\n".join(sorted(topic_timestamps)))

# %%
