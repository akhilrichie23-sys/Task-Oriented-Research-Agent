import unittest
from src.cache.semantic_cache import SemanticCache
from src.utils.cost_tracker import CostTracker

class TestCacheAndCostTracker(unittest.TestCase):
    def test_semantic_cache(self):
        cache = SemanticCache(cache_dir=".cache_test")
        prompt = "What is agentic AI?"
        model = "gpt-4o-mini"
        
        cache.set(prompt, model, "Agentic AI response")
        cached = cache.get(prompt, model)
        self.assertEqual(cached, "Agentic AI response")

    def test_cost_tracker(self):
        tracker = CostTracker()
        cost = tracker.calculate_cost("gemini-2.5-flash", input_tokens=1000, output_tokens=1000)
        self.assertAlmostEqual(cost, 0.000375)
        
        tracker.log_cache_hit(500)
        summary = tracker.get_summary()
        self.assertEqual(summary["tokens_saved_via_cache"], 500)


if __name__ == "__main__":
    unittest.main()
