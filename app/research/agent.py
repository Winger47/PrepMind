from groq import Groq
from tavily import TavilyClient
from app.models import CompanyResearch
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv    
load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def research_company(user_id: int, company_name: str, role: str, db: Session):
    results = tavily_client.search(
        query=f"{company_name} {role} interview process tech stack culture",
        max_results=5
    )
    content = "\n".join([r["content"] for r in results["results"]])
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a company research expert. 
Analyze the search results and provide a structured report with:
1. Tech stack used
2. Interview process and style
3. Company culture
4. Preparation tips for the role
Be specific and actionable."""
            },
            {
                "role": "user",
                "content": f"Company: {company_name}\nRole: {role}\n\nSearch Results:\n{content}"
            }
        ]
    )
    
    result = response.choices[0].message.content
    
    research = CompanyResearch(
        user_id=user_id,
        company_name=company_name,
        role=role,
        tips=result
    )
    db.add(research)
    db.commit()
    db.refresh(research)
    
    return research