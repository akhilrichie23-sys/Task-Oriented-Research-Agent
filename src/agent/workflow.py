from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState
from src.tools.search_tool import WebSearchTool
from src.agent.router import ModelRouter
from src.utils.logger import AuditLogger

class ResearchWorkflow:
    def __init__(self, router: ModelRouter, logger: AuditLogger):
        self.router = router
        self.logger = logger
        self.search_tool = WebSearchTool()
        self.workflow = self._build_graph()

    def _generate_queries_node(self, state: AgentState) -> dict:
        prompt = f"Deconstruct this research brief into 2 distinct web search queries: '{state['research_topic']}'."
        system_prompt = "Output only the search queries, separated by newlines."
        
        # Lightweight model route
        queries_text = self.router.call_llm(prompt, system_prompt, tier="light")
        queries = [q.strip() for q in queries_text.split("\n") if q.strip() and not q.startswith("```")]
        
        print(f"🔍 [Search Planner] Generated Queries:")
        for q in queries:
            print(f"   • \"{q}\"")
        
        self.logger.log_step("Generated Search Queries", {"queries": queries})
        return {"search_queries": queries}

    def _execute_search_node(self, state: AgentState) -> dict:
        findings = []
        print(f"\n🌐 [Web Search] Fetching live web sources...")
        for query in state["search_queries"]:
            print(f"   🔎 Searching for: '{query}'...")
            results = self.search_tool.search(query, max_results=2)
            for res in results:
                print(f"      ↳ Found: {res.get('title', 'Unknown')} ({res.get('url', '')})")
            findings.extend(results)
            
        print(f"   ✅ Collected {len(findings)} live sources.\n")
        self.logger.log_step("Executed Live Search", {"results_count": len(findings)})
        return {"raw_findings": findings}

    def _synthesize_report_node(self, state: AgentState) -> dict:
        context = "\n\n".join([f"Source: {f['url']}\nContent: {f['content']}" for f in state["raw_findings"]])
        prompt = f"Topic: {state['research_topic']}\n\nSearch Context:\n{context}\n\nSynthesize a structured, decision-ready research brief."
        system_prompt = "You are an expert technical strategist. Provide executive insights with clear citations."
        
        # Heavy model route for decision synthesis
        report = self.router.call_llm(prompt, system_prompt, tier="heavy")
        self.logger.log_step("Synthesized Report", {"report_length": len(report)})
        return {"synthesized_report": report}

    def _build_graph(self):
        builder = StateGraph(AgentState)
        
        builder.add_node("plan_queries", self._generate_queries_node)
        builder.add_node("run_search", self._execute_search_node)
        builder.add_node("build_report", self._synthesize_report_node)
        
        builder.add_edge(START, "plan_queries")
        builder.add_edge("plan_queries", "run_search")
        builder.add_edge("run_search", "build_report")
        builder.add_edge("build_report", END)
        
        return builder.compile()

    def run(self, topic: str) -> dict:
        initial_state: AgentState = {
            "research_topic": topic,
            "search_queries": [],
            "raw_findings": [],
            "synthesized_report": ""
        }
        return self.workflow.invoke(initial_state)
