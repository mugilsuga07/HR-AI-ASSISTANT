Overview
Mugil is an interactive, agentic AI-powered Streamlit application designed to help HR professionals automate the hiring plan for startup or tech roles.

This tool allows users to:
Input one or more roles they want to hire
Automatically clarify essential hiring details such as salary, skills, and timeline
Generate high-quality job descriptions
Create week-by-week hiring checklists
Draft emails to kickstart the hiring process
Built using LangGraph, OpenAI, and Streamlit.

Features
Role-based job input (example: "I want to hire an AI Engineer")
Smart clarifying questions for salary, skills, and timeline
Markdown-based job descriptions
Weekly hiring plan checklists
Email generation for internal teams
Streamlit UI with consistent styling


Tech Stack
Language model: OpenAI GPT via LangChain
Workflow orchestration: LangGraph using StateGraph for multi-node execution
Frontend: Streamlit with custom CSS for layout and styling
Search fallback: Google Search using LangChain's community wrapper
Email writer: Templated function to send across teams
