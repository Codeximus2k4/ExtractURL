from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from langchain.document_loaders import TextLoader
import textwrap
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
import os
load_dotenv()
def wrap_text_preserve_newlines(text,width=110):
  lines = text.split('\n')
  wrapped_lines = [textwrap.fill(line, width = width) for line in lines]
  astring =""
  for line in wrapped_lines:
    astring = astring + line
  return astring



url = "https://www.cucas.cn/china_scholarships/SIAS-University_Summer-Camp_scholarship_1337_81063"
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"}
r =requests.get(url, verify=False)
html = r.text
soup = BeautifulSoup(html, "html.parser")
for element in soup(
        ["header", "footer", "nav", "script", "style", "button"]
    ):
        element.extract()
text = soup.text 

with open("scholarship.txt","w",encoding="utf8") as f:
       f.write(text)
f.close()

llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
loader = TextLoader('scholarship.txt',encoding="utf8")
documents= loader.load()  
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents) 

embeddings  = HuggingFaceEmbeddings()

db =  FAISS.from_documents(docs,embeddings)

chain = load_qa_chain(llm, chain_type = "stuff")
query = "Deadline"
docs = db.similarity_search(query)
print(chain.run(input_documents=docs, question = query))


