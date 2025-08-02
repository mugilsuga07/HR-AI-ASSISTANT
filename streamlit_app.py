import os
import streamlit as st
import sys
from agent.graph import get_graph



st.set_page_config(page_title="Mugil - AI HR Assistant", layout="centered")

st.markdown("""
    <div style='text-align: center; margin-top: 50px;'>
        <h1 style='font-weight: bold; color: #FADADD;'>👩‍💼 Mugil</h1>
        <h3 style='color: #FADADD;'>Your AI-powered HR Assistant</h3>
    </div>
""", unsafe_allow_html=True)




st.write("")  
st.write("")  
st.markdown("""
    <style>
        body {
            background-color: #362F32;
            color: #FADADD;
        }
        .stApp {
            background-color: #362F32;
        }
        .stTextInput > div > div > input {
            background-color: #FFFFFF;
            color: #000000;
        }
        .stButton > button {
            background-color: #7E2A53;
            color: white;
            font-weight: bold;
            border: 1px solid #BA71A2;
            padding: 0.5em 2em;
            border-radius: 5px;
        }
        .stButton > button:hover {
            background-color: #BA71A2;
            color: #fff;
        }
        .title {
            color: #FADADD;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)




if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.role = ""
    st.session_state.salary = ""
    st.session_state.skills = ""
    st.session_state.timeline = ""
    st.session_state.result = None


if st.session_state.stage == "start":
    st.write("### What role do you want to hire for?")
    role = st.text_input(" ", key="role_input")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Generate Hiring Plan") and role:
            st.session_state.role = role
            st.session_state.stage = "clarify_salary"
            st.rerun()

elif st.session_state.stage == "clarify_salary":
    st.write(f"Great! Let's clarify a few things for: `{st.session_state.role}`")
    salary = st.text_input("What’s the annual budget (USD)?", key="salary_input")
    if salary:
        st.session_state.salary = salary
        st.session_state.stage = "clarify_skills"
        st.rerun()

elif st.session_state.stage == "clarify_skills":
    skills = st.text_input("What key skills are needed?", key="skills_input")
    if skills:
        st.session_state.skills = skills
        st.session_state.stage = "clarify_timeline"
        st.rerun()

elif st.session_state.stage == "clarify_timeline":
    timeline = st.text_input("What’s your desired hiring timeline?", key="timeline_input")
    if timeline:
        st.session_state.timeline = timeline
        st.session_state.stage = "final_submit"
        st.rerun()

elif st.session_state.stage == "final_submit":
    if st.button("Submit Details"):
        graph = get_graph()
        prompt = f"I want to hire a {st.session_state.role}"
        input_data = {
            "user_input": prompt,
            "hr_questions": {
                st.session_state.role: {
                    "budget": st.session_state.salary,
                    "skills": [s.strip() for s in st.session_state.skills.split(",")],
                    "timeline": st.session_state.timeline
                }
            }
        }
        with st.spinner("Generating hiring plan..."):
            result = graph.invoke(input_data)
            st.session_state.result = result
            st.session_state.stage = "result"
            st.rerun()

elif st.session_state.stage == "result":
    result = st.session_state.result
    role = st.session_state.role
    st.success("Hiring plan generated!")

    if st.button("View Job Description"):
        st.markdown(result.get("job_descriptions", {}).get(role, "No JD available."), unsafe_allow_html=True)

    if st.button("View Hiring Checklist"):
        st.markdown(result.get("checklists", {}).get(role, "No checklist available."), unsafe_allow_html=True)

    if st.button("View Email Draft"):
        st.markdown(result.get("emails", {}).get(role, "No email available."), unsafe_allow_html=True)








