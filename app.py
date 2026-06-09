import streamlit as st
from openai import OpenAI
from duckduckgo_search import DDGS
from pydantic import BaseModel, Field

# --- CONFIGURATION & UI SETUP ---
st.set_page_config(page_title="Adverse Media Copilot", layout="wide")

st.title("🛡️ Adverse Media & Negative News Screening Copilot (Groq Powered)")
st.caption("Explainable AI-Assisted Compliance Workflow Engine")
st.markdown("---")

# Sidebar Configuration
st.sidebar.header("⚙️ Settings")
# Make sure to replace this with your real Groq API key!
groq_api_key = "PASTE_YOUR_API_KEY_HERE"

# Hardcoded to Groq's active, supported 70B model for guaranteed JSON compliance
selected_model = "llama-3.3-70b-versatile"
st.sidebar.success(f"Locked on Active Model: {selected_model}")

# --- DATA STRUCTURES ---
class RiskAnalysis(BaseModel):
    is_relevant_match: bool = Field(description="True if the news hits target the exact entity requested, False if it is a different person/company.")
    risk_category: str = Field(description="AML, Counter-Terrorist Financing, Fraud, Regulatory Sanctions, Reputational Risk, or None.")
    risk_score: int = Field(description="Risk rating strictly from 1 (Clean) to 10 (Critical Escalation).")
    executive_summary: str = Field(description="A concise, factual 3-sentence summary of the adverse background findings.")
    justification: str = Field(description="A detailed breakdown explaining why this risk score was assigned.")

# --- BACKEND FUNCTIONS ---
def search_adverse_media(entity_name: str, context: str = "") -> list:
    """Fetches live web hits, with a bulletproof Mock Data fallback for hackathon demos."""
    query = f'"{entity_name}" {context} (fraud OR investigation OR lawsuit OR arrest OR AML OR corruption OR fine)'
    
    # 1. Try Live Search First
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5, backend="lite"))
            
            if results:
                formatted_results = []
                for r in results:
                    formatted_results.append({
                        'title': r.get('title', 'No Title'),
                        'source': r.get('href', 'Web Source'),
                        'url': r.get('href', ''),
                        'body': r.get('body', '')
                    })
                return formatted_results
    except Exception as e:
        print(f"Live search failed: {e}")
        # Ignore error and fall through to mock data

    # 2. Hackathon Fallback (Mock Data if Live Search returns [] or fails)
    st.toast("Live search blocked. Engaging Demo Mode Data.", icon="⚠️")
    
    name_lower = entity_name.lower()
    
    if "enron" in name_lower:
        return [
            {"title": "Enron Scandal: The Fall of a Wall Street Darling", "source": "Finance Weekly", "url": "https://example.com", "body": "The Enron scandal was an accounting scandal involving Enron Corporation. Executives hid billions in debt from failed deals and projects."},
            {"title": "Former Enron CEO indicted for fraud", "source": "News Corp", "url": "https://example.com", "body": "Jeffrey Skilling and Kenneth Lay were indicted on charges of wire fraud, securities fraud, and insider trading related to the massive corporate collapse."}
        ]
    elif "ftx" in name_lower:
        return [
            {"title": "FTX Founder Arrested on Fraud Charges", "source": "Crypto News", "url": "https://example.com", "body": "The founder of FTX was arrested after US prosecutors filed criminal charges including wire fraud, money laundering, and campaign finance violations."},
            {"title": "Billions Missing in FTX Collapse", "source": "Market Watch", "url": "https://example.com", "body": "Customer funds were allegedly commingled with Alameda Research, leading to a massive liquidity crisis and the ultimate bankruptcy of the exchange."}
        ]
    elif "worldcom" in name_lower:
        return [
            {"title": "WorldCom Files for Bankruptcy in Massive Fraud Case", "source": "Business Insider", "url": "https://example.com", "body": "Telecommunications giant WorldCom filed for Chapter 11 bankruptcy after revealing it had inflated assets by over $11 billion in a massive accounting fraud scheme."}
        ]
    else:
        # If it's a random name and live search failed, return empty
        return []

def analyze_entity_risk(entity_name: str, search_hits: list, api_key: str, model: str) -> RiskAnalysis:
    """Analyzes search hits using Groq's JSON mode."""
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    formatted_hits = ""
    for idx, hit in enumerate(search_hits):
        formatted_hits += f"[{idx+1}] Title: {hit['title']}\nSource: {hit['source']}\nSnippet: {hit['body']}\n\n"

    prompt = f"""
    You are an expert Compliance, AML, and Risk Intelligence Analyst.
    Review background media checks for the target entity: "{entity_name}".
    Determine if the text refers to our target entity. Assign a risk rating (1-10) and category.
    
    You must output your response as a strict JSON object matching this schema:
    {{
        "is_relevant_match": bool,
        "risk_category": "string",
        "risk_score": int,
        "executive_summary": "string",
        "justification": "string"
    }}

    Search Results Content:
    {formatted_hits}
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a precise compliance automation system that outputs JSON only."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    
    raw_json = response.choices[0].message.content
    return RiskAnalysis.model_validate_json(raw_json)

# --- STREAMLIT USER INTERFACE ---
col1, col2 = st.columns([2, 1])

with col1:
    entity_name = st.text_input("Entity Target Name", placeholder="e.g., Wirecard, Enron, Theranos")
with col2:
    context = st.text_input("Optional Context / Location", placeholder="e.g., Germany, Tech")

if st.button("Run Screening Profile", type="primary"):
    if groq_api_key == "PASTE_YOUR_GROQ_API_KEY_HERE" or not groq_api_key:
        st.error("Please insert your real Groq API Key into the `app.py` code.")
    elif not entity_name:
        st.warning("Please enter an entity name to screen.")
    else:
        with st.spinner("Executing live adverse media scanning and risk generation..."):
            hits = search_adverse_media(entity_name, context)
            
            if hits is None:
                st.warning("Screening paused due to search API limits.")
            elif len(hits) == 0:
                st.success(f"Clear Profile: No immediate adverse media footprints found for '{entity_name}'.")
            else:
                try:
                    # Calling the globally defined function
                    analysis_result = analyze_entity_risk(entity_name, hits, groq_api_key, selected_model)
                    
                    st.subheader("📊 Screening Decision Engine Output")
                    
                    m_col1, m_col2, m_col3 = st.columns(3)
                    with m_col1:
                        st.metric("Risk Score", f"{analysis_result.risk_score} / 10")
                    with m_col2:
                        st.metric("Risk Category", analysis_result.risk_category)
                    with m_col3:
                        match_status = "✅ Confirmed Match" if analysis_result.is_relevant_match else "❓ Unverified/False Match"
                        st.metric("Entity Resolution", match_status)
                    
                    st.markdown("### 📝 Executive Summary")
                    st.info(analysis_result.executive_summary)
                    
                    st.markdown("### 🔍 Explainable Justification & Audit Trail")
                    st.write(analysis_result.justification)
                    
                    st.markdown("### 📑 Traceable Sources Reviewed")
                    for idx, hit in enumerate(hits):
                        with st.expander(f"[{idx+1}] {hit['title']}"):
                            st.write(f"**Snippet:** {hit['body']}")
                            st.markdown(f"[View Original Source Article]({hit['url']})")
                    
                    st.markdown("---")
                    st.markdown("### 🛠️ Reviewer Workflow Actions")
                    action_col1, action_col2 = st.columns(2)
                    with action_col1:
                        if st.button("✅ Approve Profile & Archive"):
                            st.success("Profile safely logged.")
                    with action_col2:
                        if st.button("🚨 Escalate to Compliance Committee"):
                            st.error("Profile flagged.")
                            
                except Exception as parse_error:
                    st.error(f"Failed to analyze data or generate valid JSON: {parse_error}")