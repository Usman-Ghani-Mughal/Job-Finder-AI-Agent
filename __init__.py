import os
# from langchain.llms import LlamaCpp
from langchain.chains import LLMChain
#from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import AzureChatOpenAI
import utils as ut
import prompts.prompts_template as prom
from dotenv import load_dotenv
load_dotenv()
