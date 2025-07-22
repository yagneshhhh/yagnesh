import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm=ChatGroq(temperature=0,groq_api_key=os.getenv("GROQ_API_KEY"),model="meta-llama/llama-4-maverick-17b-128e-instruct")

    def extract_jobs(self,clean_text):
        prompt_extract=PromptTemplate.from_template("""
         ###SCRAPED TEXT FROM WEBSITE:
            {page_data},
         ###INSTRUCTIONS:
            The scraped text is from a job posting site .your job is to extract the  job postings and return them in a json format containing following 
            key roles : 'role ' , 'experience',' skills '   and 'description ' . only return valid JSON .
        ### VALID JSON (NO PREAMBLE) :
        """)
        chain_extract=prompt_extract | self.llm
        res=chain_extract.invoke(input={"page_data":clean_text})
        try:
            json_parser=JsonOutputParser()
            res=json_parser.parse(res.content)
        except:
            raise outputParserException("context is too big. unable to extract job postings")
        return res if isinstance(res,list) else [res]
    def write_email(self, job ,links ):
        email_prompt=PromptTemplate.from_template("""
        ###JOB DESCRIPTION:
            {job_description}
        ### INSTRUCTION:
            You are Yagnesh , a HR at XYZ Solutions.XYZ Solutions is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of XYZ Solutions 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase XYZ's portfolio: {links}
            Remember you are Yagnesh, HR at XYZ my . 
            Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):""")
        email_extract= email_prompt | self.llm
        email_res=email_extract.invoke(input={"job_description":str(job),"links":links})
        return email_res.content

if __name__=='__main__':
    print(os.getenv("GROQ_API_KEY"))