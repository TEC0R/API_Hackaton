import os
from dotenv import load_dotenv
from langchain_community.embeddings import SentenceTransformerEmbeddings
#from langchain.embeddings import SentenceTransformerEmbeddings
pinecone_api_key = os.getenv("PINECONE_API_KEY")
groq_api = os.getenv('GROQ_API_KEY')
load_dotenv()
import langchain
from langchain_groq import ChatGroq
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore  
from typing import List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain.chains import create_retrieval_chain
from pprint import pprint
import warnings
warnings.filterwarnings('ignore')
#########################################################################################
pc = pc = Pinecone(api_key=pinecone_api_key)
embeddings = SentenceTransformerEmbeddings(model_name='sentence-transformers/LaBSE')
vectorstore = PineconeVectorStore(index_name='hackathon', embedding=embeddings)
########################################################################################
def read_system_prompt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
file_path = './GET/system_prompt.txt'

class jobs(BaseModel):
    nom : list[str] = Field(description="the name of the person")
    contact : list[str] = Field(description="a list of contact, like email, phone number or adress")
    metier : list[str] = Field(description="the job or expertise of the person")
    skills : list[str] = Field(description="list of skills for the mentor")
    dispo : list[str] = Field(description="the availability of the person, if true then yes if false then no")
    asso : list[str] = Field(description="the company name, and the description")



#output parser : define how we want data get back from llm
parser  = JsonOutputParser(pydantic_object=jobs)

template = read_system_prompt(file_path)
prompt = ChatPromptTemplate.from_template(template,
                                           partial_variables={"format_instruction": parser.get_format_instructions()} )
def chat_groq(t = 0, choix ="llama3-70b-8192", api = groq_api) : #choix peu prendre : llama3-8b-8192 ,mixtral-8x7b-32768, gemma-7b-it
    return ChatGroq(temperature = t, model_name=choix,groq_api_key = api)


model_chat = chat_groq()
document_chain = create_stuff_documents_chain(model_chat, prompt,output_parser=parser)

#get db as retriever
retriever = vectorstore.as_retriever()
#create chain of retreival
retriever_chain  = create_retrieval_chain(retriever,document_chain)
def reco_mentor(text):
    response = retriever_chain.invoke({"input": text})
    return response['answer']
