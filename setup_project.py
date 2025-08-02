import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    "src/agent/__init__.py",
    "src/agent/graph.py", #LangGraph logic

    "src/tools/__init__.py",
    "src/tools/search.py",         
    "src/tools/email.py",          

  
    ".env",                      
    ".gitignore",
    "README.md",
    "requirements.txt",
    "streamlit_app.py",           

  
]

for filepath in list_of_files:
    path = Path(filepath)
    filedir = path.parent

    if not filedir.exists():
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir}")

    if not path.exists() or path.stat().st_size == 0:
        with open(path, "w") as f:
            if path.suffix == ".py":
                f.write(f"# {path.name}\n\n")
            elif path.name == ".env":
                f.write("OPENAI_API_KEY=\nGOOGLE_API_KEY=\nGOOGLE_CSE_ID=\n")
        logging.info(f"Created file: {filepath}")
    else:
        logging.info(f"⚠️ Skipped existing file: {filepath}")
