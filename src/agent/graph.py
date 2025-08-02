import json
from dotenv import load_dotenv
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, END

from src.agent.state import AgentState, get_missing_fields, initialize_questions
from src.tools.search import google_search_tool
from src.tools.email import write_email

load_dotenv()
llm = ChatOpenAI(temperature=0)

#prompts 
clarify_prompt = PromptTemplate.from_template("""
You are an HR compensation advisor for a competitive U.S. tech company hiring for: {role}.  
Provide realistic but **top-tier market-rate estimates** for:  
- Salary (monthly, USD)  
- Key skills required  
- Hiring timeline  
Assume:  
- The company pays in the **75th–90th percentile** for talent  
- Role is based in a **high-cost tech hub** (SF/NYC/Seattle)  
Respond **strictly in JSON**:  
{{
  "budget": "[monthly base salary in USD]",  
  "skills": ["list", "of", "3–5", "critical", "skills"],  
  "timeline": "typical hiring timeframe"  
}}  
""")

jd_prompt = PromptTemplate.from_template("""
You are a professional HR content writer helping draft a high-quality job description.

Write a structured, engaging, and realistic job description for the following role:

- **Role**: {role}
- **Skills Required**: {skills}
- **Salary**: {budget} USD
- **Hiring Timeline**: {timeline}

Include:
1. A 2–3 sentence summary
2. 5–7 key responsibilities
3. 5–7 qualifications
4. Salary & timeline note

Format in **Markdown**
""")

checklist_prompt = PromptTemplate.from_template("""
You are an HR assistant helping create a weekly hiring plan for:

- Role: {role}
- Timeline: {timeline}
- Skills: {skills}
- Budget: {budget}

Output a Markdown-formatted week-by-week checklist.
""")

#specifying all nodes

def clarify_hr_questions(state: AgentState) -> AgentState:
    if "hr_questions" not in state:
        state["hr_questions"] = initialize_questions(state["user_input"])

    missing_fields = get_missing_fields(state["hr_questions"])
    for role, fields in missing_fields.items():
        prompt = clarify_prompt.format(role=role)
        response = llm.predict(prompt)
        try:
            answers = json.loads(response)
        except json.JSONDecodeError:
            print(f"[WARN] Invalid JSON for role '{role}':\n{response}")
            answers = {}

        for field in fields:
            if field not in answers or not answers[field]:
                query = f"{role} {field} in tech industry"
                print(f"\n🔍 [Google Search Fallback] Querying: {query}")
                try:
                    result = google_search_tool.func(query)
                    answers[field] = result[:300]
                except Exception as e:
                    print(f"⚠️ Google search failed: {e}")
                    answers[field] = "Search failed."

        for field in fields:
            if field in answers:
                state["hr_questions"][role][field] = answers[field]

    return state


def generate_job_descriptions(state: AgentState) -> AgentState:
    state["job_descriptions"] = {}
    for role, data in state["hr_questions"].items():
        budget_raw = data.get("budget", "N/A")
        try:
            budget = int(budget_raw.strip().replace(",", "").replace("$", ""))
            budget_formatted = f"${budget:,} per year"
        except:
            budget_formatted = budget_raw

        skills = ", ".join(data.get("skills", [])) if isinstance(data.get("skills"), list) else data.get("skills", "")
        prompt = jd_prompt.format(
            role=role,
            skills=skills,
            budget=budget_formatted,
            timeline=data.get("timeline", "N/A")
        )
        jd = llm.predict(prompt)
        state["job_descriptions"][role] = jd
    return state


def generate_checklists(state: AgentState) -> AgentState:
    state["checklists"] = {}
    for role, data in state["hr_questions"].items():
        prompt = checklist_prompt.format(
            role=role,
            skills=", ".join(data.get("skills", [])) if isinstance(data.get("skills"), list) else data.get("skills", ""),
            budget=data.get("budget", "N/A"),
            timeline=data.get("timeline", "N/A")
        )
        checklist = llm.predict(prompt)
        state["checklists"][role] = checklist
    return state


def generate_email(state: AgentState) -> AgentState:
    state["emails"] = {}
    for role in state["job_descriptions"]:
        jd = state["job_descriptions"].get(role, "")
        cl = state["checklists"].get(role, "")
        if jd and cl:
            email = write_email(role, jd, cl)
            state["emails"][role] = email
        else:
            state["emails"][role] = "Email content could not be generated."
    return state


def format_questions(state: AgentState) -> AgentState:
    questions = state["hr_questions"]
    output = []
    for role, data in questions.items():
        skills = ", ".join(data.get("skills", [])) if isinstance(data.get("skills"), list) else data.get("skills", "")
        output.append(f"### {role} Role")
        output.append(f"- Budget: {data.get('budget', 'N/A')}")
        output.append(f"- Skills: {skills}")
        output.append(f"- Timeline: {data.get('timeline', 'N/A')}")
        output.append("")
    state["output"] = "\n".join(output)
    return state

#LangGraph

def get_graph():
    builder = StateGraph(AgentState)
    builder.add_node("clarify", clarify_hr_questions)
    builder.add_node("format", format_questions)
    builder.add_node("generate_jd", generate_job_descriptions)
    builder.add_node("generate_checklists", generate_checklists)
    builder.add_node("generate_email", generate_email)

    builder.set_entry_point("clarify")
    builder.add_edge("clarify", "format")
    builder.add_edge("format", "generate_jd")
    builder.add_edge("generate_jd", "generate_checklists")
    builder.add_edge("generate_checklists", "generate_email")
    builder.add_edge("generate_email", END)

    return builder.compile()


if __name__ == "__main__":
    graph = get_graph()
    user_input = input("💬 What roles do you want to hire for?\n> ")
    result = graph.invoke({"user_input": user_input})

    print("\nFinal Output:\n")
    print(result.get("output", "[No formatted output]"))

    if "job_descriptions" in result:
        print("\nJob Descriptions:\n")
        for role, jd in result["job_descriptions"].items():
            print(f"\n### {role} JD\n{jd}")

    if "checklists" in result:
        print("\nHiring Checklists:\n")
        for role, cl in result["checklists"].items():
            print(f"\n### {role} Checklist\n{cl}")

    if "emails" in result:
        print("\nEmails:\n")
        for role, email in result["emails"].items():
            print(f"\n### Email for {role}\n{email}")





