from typing import TypedDict, Dict, List

# Agent state schema
class AgentState(TypedDict, total=False):
    user_input: str
    hr_questions: Dict[str, Dict[str, str]]
    output: str
    job_descriptions: Dict[str, str]
    checklists: Dict[str, str]
    emails: Dict[str, str]  

# Required fields for every role
required_fields = ["budget", "skills", "timeline"]


def get_missing_fields(questions: Dict[str, Dict[str, str]]) -> Dict[str, List[str]]:
    missing = {}
    for role, data in questions.items():
        fields = [f for f in required_fields if not data.get(f)]
        if fields:
            missing[role] = fields
    return missing


def initialize_questions(user_input: str) -> Dict[str, Dict[str, str]]:
    if "hire" in user_input:
        raw = user_input.split("hire")[1]
        roles = [r.strip() for r in raw.split("and")]
    else:
        roles = [user_input.strip()]
    return {role: {f: "" for f in required_fields} for role in roles}
