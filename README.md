Mugil: AI-Powered Hiring Assistant

Mugil is an interactive, AI-driven tool designed to automate and streamline the hiring process for HR professionals, especially in startups and tech environments. Built with OpenAI and LangChain, and orchestrated via LangGraph, it generates job descriptions, hiring checklists, and recruitment emails through an intelligent, agentic workflow.

Link to the the app: https://hr-ai-assistant-gybgrfun6na2nftufi7sgf.streamlit.app

Architectural Diagram

It simplifies HR workflows by:
Providing guided input with clarifying questions (salary, skills, timelines).
Automatically generating outputs:
Markdown-formatted job descriptions.
Week-by-week hiring checklists.
Internal recruitment emails.
Using agentic AI with LangGraph’s stateful workflow to break tasks into steps, retry missing info, and fall back to Google Search when needed.

Agentic Components:

LangGraph:
Defines step-by-step workflow (StateGraph).
Acts as a finite-state planner.

AgentState:
Shared memory across steps.
Ensures continuity between actions.

Prompt-driven Nodes:
Each task (JD, checklist, email) is a reasoning step.
Enables modular autonomy.

Fallback Search:
Queries Google if LLM fails.
Uses external tools for robustness.

Clarification Logic:
Detects missing data and reprompts.
Self-monitoring capability.



