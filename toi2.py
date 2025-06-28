import asyncio
import re

import pandas as pd
import datetime
from browser_use import Agent
from langchain_community.chat_models import AzureChatOpenAI

import os
import sys


import setup_playwright
setup_playwright.install_playwright()

import streamlit as st

# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Windows-specific fix for asyncio
# asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
if os.name == 'nt':
	asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.set_page_config(page_title="TOI ePaper Summarizer", layout="wide")
st.title("🗞️ Times of India Front Page Summarizer")

# Get date input from user
selected_date = st.date_input("📅 Select the ePaper date", value=datetime.date.today(), max_value=datetime.date.today())

# Optional: user must click to start
if st.button("🔍 Summarize Front Page"):
    with st.spinner("Running Agent and fetching summaries..."):

        # Format the task to pass to LLM
        task_description = f'''Go to the ePaper of timesofindia for the date {selected_date.strftime("%B %d, %Y")}. 
Use my Google account to login if required.
username - ravi6389@gmail.com
password - ravi100!

		Once you log in, do the following :
        1. switch to digital view. 
        2. Click on the calendar on top right of screen to select the date that user has asked for.
        2. Extract the headline , article of top 2 articles from the section of 'Front Page' and summarize them as well.
        3.Finally show the data in a table format showing Headline, Full article and summary of articles in 3 columns.
'''

        def extract_table_from_llm_response(response_text: str) -> pd.DataFrame:
            match = re.search(r'\|.*?\|\n\|[-| ]+\|\n(?:\|.*?\|\n?)+', response_text, re.DOTALL)
            if not match:
                st.error("No markdown table found in the LLM response.")
                return pd.DataFrame()
            table_markdown = match.group(0)
            try:
                from io import StringIO
                return pd.read_csv(StringIO(table_markdown), sep="|", engine='python', skipinitialspace=True).dropna(axis=1, how='all')
            except Exception as e:
                st.error(f"Error parsing markdown table: {e}")
                return pd.DataFrame()

        async def main():
            llm = AzureChatOpenAI(
        api_key = "6FlSZ2qDwe9kfsTaEIPb8PRUCRmNyhS2AIIDduT1hsi54ap2dYeAJQQJ99BFACHYHv6XJ3w3AAAAACOGV2L9",
                        azure_endpoint = "https://learn-mcboa439-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview",
                        model = "gpt-4o",
                        api_version="2024-02-15-preview",
                        temperature = 0.
    # other params...
            ) 

            agent = Agent(
                task=task_description,
                llm=llm,
            )

            await agent.run()

           

        asyncio.run(main())
