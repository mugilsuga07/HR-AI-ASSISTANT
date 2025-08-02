import os
from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper

load_dotenv()

#Created a search wrapper using the loaded keys
search = GoogleSearchAPIWrapper(
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    google_cse_id=os.getenv("GOOGLE_CSE_ID")
)


def tracked_search(query: str) -> str:
    print(f"\n🔍 [Google Search] Querying: {query}")
    return search.run(query)

google_search_tool = Tool(
    name="google_search",
    description="Search Google for recent and relevant information.",
    func=tracked_search,
)


