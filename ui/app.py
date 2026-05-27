import streamlit as st
import requests

st.set_page_config(
    page_title="Job Market Intelligence Agent",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Job Market Intelligence Agent")
st.markdown("*AI-powered career gap analysis using live job market data*")

st.sidebar.header("Your Profile")
role = st.sidebar.selectbox(
    "Target Role",
    ["Data Scientist", "ML Engineer", "NLP Engineer", 
     "GenAI Engineer", "Data Analyst"]
)

user_skills_input = st.sidebar.text_area(
    "Your Current Skills (comma separated)",
    placeholder="Python, SQL, Pandas, Machine Learning"
)

analyze_btn = st.sidebar.button("🚀 Analyze My Profile", type="primary")

if analyze_btn:
    if not user_skills_input:
        st.error("Please enter your skills first.")
    else:
        query = f"Analyze {role} market for my skills: {user_skills_input}"
        
        with st.spinner("Agent is analyzing live job market... Please wait"):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    json={"query": query}
                )
                data = response.json()
                
                # Top metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Target Role", data["role"])
                with col2:
                    st.metric("Jobs Analyzed", data["total_jobs_analyzed"])
                with col3:
                    st.metric("Your Skills", len(data["user_skills"]))
                
                st.divider()
                
                # Skills comparison
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("✅ Your Skills")
                    for skill in data["user_skills"]:
                        st.success(skill)
                
                with col2:
                    st.subheader("📈 Top Market Skills")
                    for skill in data["top_market_skills"][:8]:
                        if skill in data["user_skills"]:
                            st.success(f"{skill} ✓")
                        else:
                            st.warning(f"{skill} ← Learn this")
                
                st.divider()
                
                # Final report
                st.subheader("📋 Your Career Report")
                st.markdown(data["final_report"])
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
else:
    st.info("👈 Enter your skills in the sidebar and click Analyze")