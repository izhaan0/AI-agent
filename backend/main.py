from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import psycopg2
import redis
import json
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection (PostgreSQL)
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

# Redis connection for caching
redis_client = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)

# LinkedIn API credentials
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"

# OpenAI setup with LangChain
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")

# Pydantic models
class UserProfile(BaseModel):
    user_id: str
    skills: list
    experience: list
    interests: list

class PostContent(BaseModel):
    content: str
    scheduled_time: str

# LinkedIn OAuth 2.0 Authentication
@app.get("/auth/linkedin")
async def auth_linkedin():
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?response_type=code"
        f"&client_id={LINKEDIN_CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&scope=r_liteprofile%20w_member_social"
    )
    return {"auth_url": auth_url}

@app.get("/callback")
async def callback(code: str):
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get access token")
    access_token = response.json().get("access_token")
    redis_client.setex(f"token_{code}", timedelta(hours=1), access_token)
    return {"access_token": access_token}

# Profile Analysis
@app.post("/analyze_profile")
async def analyze_profile(profile: UserProfile):
    cursor.execute(
        "INSERT INTO profiles (user_id, skills, experience, interests) VALUES (%s, %s, %s, %s)",
        (profile.user_id, json.dumps(profile.skills), json.dumps(profile.experience), json.dumps(profile.interests))
    )
    conn.commit()
    
    prompt = PromptTemplate(
        input_variables=["skills", "experience", "interests"],
        template="Summarize a professional profile with skills: {skills}, experience: {experience}, interests: {interests}."
    )
    summary = llm(prompt.format(skills=profile.skills, experience=profile.experience, interests=profile.interests))
    return {"summary": summary}

# Content Generation
@app.post("/generate_post")
async def generate_post(profile: UserProfile):
    trends = ["AI in marketing", "Personal branding in 2025", "Social media analytics"]
    prompt = PromptTemplate(
        input_variables=["profile_summary", "trends"],
        template="Create a LinkedIn post for a professional with this profile: {profile_summary}. Incorporate these industry trends: {trends}. Keep it engaging, professional, and under 280 characters."
    )
    profile_summary = f"Skills: {', '.join(profile.skills)}, Experience: {', '.join(profile.experience)}, Interests: {', '.join(profile.interests)}"
    post_content = llm(prompt.format(profile_summary=profile_summary, trends=", ".join(trends)))
    
    optimized_content = f"{post_content} #PersonalBranding #IndustryTrends"
    
    cursor.execute(
        "INSERT INTO posts (user_id, content, created_at) VALUES (%s, %s, %s)",
        (profile.user_id, optimized_content, datetime.now())
    )
    conn.commit()
    
    return {"post_content": optimized_content}

# Automated Posting
@app.post("/schedule_post")
async def schedule_post(post: PostContent, user_id: str):
    access_token = redis_client.get(f"token_{user_id}")
    if not access_token:
        raise HTTPException(status_code=401, detail="No valid access token")
    
    headers = {"Authorization": f"Bearer {access_token.decode()}"}
    post_data = {
        "author": f"urn:li:person:{user_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post.content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers=headers,
        json=post_data
    )
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Failed to post to LinkedIn")
    
    cursor.execute(
        "UPDATE posts SET posted_at = %s WHERE content = %s",
        (post.scheduled_time, post.content)
    )
    conn.commit()
    
    return {"status": "Post scheduled"}

# Performance Analytics
@app.get("/analytics/{user_id}")
async def get_analytics(user_id: str):
    cursor.execute(
        "SELECT content, created_at, posted_at FROM posts WHERE user_id = %s",
        (user_id,)
    )
    posts = cursor.fetchall()
    analytics = [{"content": p[0], "created_at": p[1], "posted_at": p[2]} for p in posts]
    return {"analytics": analytics}

# Initialize database tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        user_id VARCHAR PRIMARY KEY,
        skills JSONB,
        experience JSONB,
        interests JSONB
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR,
        content TEXT,
        created_at TIMESTAMP,
        posted_at TIMESTAMP
    )
""")
conn.commit()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)