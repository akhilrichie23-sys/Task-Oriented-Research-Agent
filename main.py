import os
from dotenv import load_dotenv
from src.utils.cost_tracker import CostTracker
from src.utils.logger import AuditLogger
from src.cache.semantic_cache import SemanticCache
from src.agent.router import ModelRouter
from src.agent.workflow import ResearchWorkflow

load_dotenv()

def main():
    # Initialize Core Engines
    cost_tracker = CostTracker()
    audit_logger = AuditLogger()
    cache = SemanticCache()
    router = ModelRouter(cost_tracker, cache)
    
    workflow = ResearchWorkflow(router, audit_logger)
    
    # Run Research Agent
    topic = "Key architectural trends in agentic AI frameworks for 2026"
    print(f"\n🚀 Running Autonomous Research Agent for: '{topic}'...\n")
    
    final_state = workflow.run(topic)
    
    # Display Results
    print("--- 📄 Decision-Ready Brief ---")
    print(final_state["synthesized_report"])
    print("\n------------------------------")
    
    # Display Audit & Cost Summary
    summary = cost_tracker.get_summary()
    audit_logger.log_step("Execution Finished", {"cost_summary": summary})
    
    print("\n📊 Cost & Execution Summary:")
    print(f"• Total Tokens Spent: {summary['total_tokens']}")
    print(f"• Tokens Saved via Cache: {summary['tokens_saved_via_cache']}")
    print(f"• Total Cost: ${summary['estimated_cost_usd']}")
    print(f"• Audit Log Saved to: {audit_logger.log_file}\n")

if __name__ == "__main__":
    main()
