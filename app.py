#==============LOAD MODULES==================
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np


# To show web-app: complete page layout
st.set_page_config(layout="wide")

# To Give Title
st.title("AI RESUME GENERATOR")
st.write("""This app helps user to build customized Professional Resume with Latest Job Apply Links""")

st.image("bg.png")

#============API KEY==================

GOOGLE_API_KEY= "AQ.Ab8RN6Ln9Q6bf9vmUDVVW1ZAl7AoM9-XOlNubgHOz7AKcw2cXw"
GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

#============MODEL====================
model= ChatGoogleGenerativeAI(
    model= 'gemini-3.5-flash-lite',
    google_api_key= GOOGLE_API_KEY
)

#response= model.invoke("Hello Buddy!")
#response.content[-1]['text']

def search_latest_news_jobs(query):
  """This function helps to fetch latest
  news or jobs related article using
  tavily"""

  client= TavilyClient(
      api_key= TAVILY_API_KEY)
  response= client.search(query)
  return response

#=============Agent Creation=================
agent= create_agent(
     model= model,
     tools= [search_latest_news_jobs])
agent

def main_agent(agent,query):
  """This is main agent, or leader agent
  orchestrate sub agents"""

  #Giving prompts to create  detailed prompt for code generation
  prompt= """You are AI assistant and below given a prompt, your task is to give
  detailed prompt for this.
  You are a professional Resume generator where uuser will give their personal
  information, you have to create a detailed Resume for students or professional
  one, it must be with Dynamic VI and VX and, with advanced CSS Professional
  Desining. Make sure to give output in HTML Format only no markdowns allowed"""

  response = agent.invoke({'messages': [{'role': 'user','content': prompt}]})
  detailed_prompt = response['messages'][-1].content[-1]['text']
  # SAVE PROMPT using File Handling
  with open('prompt.txt', 'w') as f:
     f.write(detailed_prompt)

  user_details= f"""Below Given is a user details generate Resume based on that,
  if not given keep:
  Default Resume: Python Developer
  user details:{query}"""
  final_prompt= prompt+ detailed_prompt + user_details

  #Code Generation

  response = agent.invoke({'messages': [{'role': 'user','content': final_prompt}]})
  code = response['messages'][-1].content[-1]['text']
  return code

#code= main_agent(agent,"JYOTI SHOKEEN, GEN AI EXPERT")
#from IPython import display as DISPLAY
#DISPLAY.HTML(code)

def get_job(agent,
           Location= "Noida, Delhi",
           Profile= "Data Analysts, AI Engineer"):
  Location = "Noida, Delhi"
  Profile = "Data Analysts, AI Engineer"

  prompt= f"""Based user given Job profile,
  fetch latest jobs or job apply article
  using Naukri, Linkdin, Indeed, or all popular
  Job apply platform , Show Results with
  JOB PROFILE NAME, EDUCATION, SALARY, COMPANY NAME,
  SHOW jobs only related to given
  {Location} and {Profile}, output must be in
  Professional HTML Naukri theme cards with Dynamic Design,
  Show atleast Top 18-20 results with direct apply link"""

  response = agent.invoke({'messages': [{'role': 'user','content': prompt}]})
  code = response['messages'][-1].content[-1]['text']

  return code

#code= get_job(agent)
#DISPLAY.HTML(code


#============API KEY==================

GOOGLE_API_KEY= "AQ.Ab8RN6Ln9Q6bf9vmUDVVW1ZAl7AoM9-XOlNubgHOz7AKcw2cXw"
GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

all_API = [TAVILY_API_KEY, GROQ_API_KEY,
GOOGLE_API_KEY]
if not all(all_API):
   st.error("Must give API keys")
   st.stop()
elif all(all_API):
   st.success("API KEYS LOADED SUCCESSFULLY")
else:
   st.info("PASS ALL API-KEYS")

#====================MULTISELECT OPTION===========================
options = ["Delhi", "Mumbai","Pune", "Banglore", "Gurugram/Gurgaon"]
location = st.sidebar.multiselect("Select Location",
options = options)
profile_op = ["Data Analysts", "AI Engineer", "Gen AI Developer", "Full-Stack Dev", "Data Scientist"]
profile = st.sidebar.multiselect("Select Job Profile",
options = profile_op)

#===================================GET USER INFO=====================================
st.markdown("""### GET USER INFO""")
user_info = st.text_area("""Write your Resume Description: """)

if st.button("Generate Resume"):
          with st.spinner("Agent Running"):
                    code = main_agent(agent, user_info)
                    st.html(code, width="stretch",
                            unsafe_allow_javascript=True)
                    st.divider() #to give horizontal div
                    job_code = get_jobs (agent, location, profile)
                    st.html(job_code, width="stretch",
                            unsafe_allow_javascript=True)
