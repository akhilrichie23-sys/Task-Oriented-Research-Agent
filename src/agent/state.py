from typing import TypedDict

class AgentState(TypedDict):
    research_topic: str
    search_queries: list[str]
    raw_findings: list[dict]
    synthesized_report: str
