import streamlit as st
import pandas as pd
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text
def create_email_app(llm,portfolio,clean_text):
    st.title ("Cold E-mail Generator")
    url=st.text_input("enter a job posting link", value='')
    submit_button=st.button("submit")
    if submit_button:
        try:
            loader = WebBaseLoader([url])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs=llm.extract_jobs(data)
            for job in jobs:
                skills=job.get('skills',[])
                links=portfolio.query_links(skills)
                email=llm.write_email(job,links)
                st.write('your email is generated ✔')
                st.code(email,language='markdown')
        except Exception as e:
            st.error(f"an error occurred:{e}")

if __name__=='__main__':
    chain=Chain()
    portfolio=Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_email_app(chain,portfolio,clean_text)