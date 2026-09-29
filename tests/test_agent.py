import unittest
from unittest.mock import MagicMock, patch
from src.agent.router import ModelRouter
from src.agent.workflow import ResearchWorkflow
from src.utils.cost_tracker import CostTracker
from src.utils.logger import AuditLogger
from src.cache.semantic_cache import SemanticCache
from src.tools.scraper_tool import WebScraperTool
from src.tools.pdf_tool import ReportGenerator

class TestAgentPipeline(unittest.TestCase):
    def setUp(self):
        self.cost_tracker = CostTracker()
        self.logger = AuditLogger(log_dir="outputs/audit_logs")
        self.cache = SemanticCache(cache_dir=".cache_test")

    def test_scraper_tool(self):
        scraper = WebScraperTool()
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.text = "<html><body><h1>Title</h1><p>Test agentic content</p></body></html>"
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response
            
            cleaned = scraper.fetch_and_clean("https://example.com")
            self.assertIn("Test agentic content", cleaned)

    def test_report_generator(self):
        generator = ReportGenerator(output_dir="outputs/reports")
        content = "# Test Title\n## Section 1\nExecutive research findings."
        
        md_file = generator.save_markdown("test_report", content)
        self.assertTrue(md_file.exists())
        
        pdf_file = generator.save_pdf("test_report", content)
        self.assertTrue(pdf_file.exists())

    @patch("src.agent.workflow.WebSearchTool")
    def test_full_workflow_mocked(self, mock_search_tool_cls):
        # Mock search tool
        mock_search_instance = MagicMock()
        mock_search_instance.search.return_value = [
            {"title": "Agentic AI 2026", "url": "https://example.com/agents", "content": "Autonomous workflows in 2026."}
        ]
        mock_search_tool_cls.return_value = mock_search_instance

        router = ModelRouter(self.cost_tracker, self.cache)

        # Mock call_llm directly
        def mock_call_llm(prompt, system_prompt, tier="light"):
            if tier == "light":
                router.tracker.calculate_cost("gemini-2.5-flash", 50, 20)
                return "Agentic AI Trends 2026\nAI Orchestration Architectures"
            else:
                router.tracker.calculate_cost("gemini-2.5-pro", 200, 100)
                return "# Executive Brief\nAutonomous agents are leading AI adoption."

        router.call_llm = MagicMock(side_effect=mock_call_llm)




        # Execute Workflow
        workflow = ResearchWorkflow(router, self.logger)
        result = workflow.run("Architectural trends in AI agents")
        
        self.assertIn("synthesized_report", result)
        self.assertIn("Executive Brief", result["synthesized_report"])
        self.assertGreater(self.cost_tracker.total_cost, 0.0)


if __name__ == "__main__":
    unittest.main()
