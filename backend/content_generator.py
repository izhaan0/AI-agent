from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")

def generate_post(profile_summary: str, trends: list):
    prompt = PromptTemplate(
        input_variables=["profile_summary", "trends"],
        template="Create a LinkedIn post for a professional with this profile: {profile_summary}. Incorporate these industry trends: {trends}. Keep it engaging, professional, and under 280 characters."
    )
    post_content = llm(prompt.format(profile_summary=profile_summary, trends=", ".join(trends)))
    return f"{post_content} #PersonalBranding #IndustryTrends"  