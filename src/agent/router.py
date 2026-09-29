import os
from google import genai
from src.cache.semantic_cache import SemanticCache
from src.utils.cost_tracker import CostTracker

class ModelRouter:
    def __init__(self, cost_tracker: CostTracker, cache: SemanticCache):
        gemini_key = os.getenv("GEMINI_API_KEY")
        self.gemini_client = genai.Client(api_key=gemini_key or "dummy-key-for-testing")
        self.tracker = cost_tracker
        self.cache = cache

    def call_llm(self, prompt: str, system_prompt: str, tier: str = "light") -> str:
        # Model tier selection (Fast/Cheap vs Reasoning)
        model_name = "gemini-3.7-flash" if tier == "light" else "gemini-3.7-flash"
        
        # 1. Check Semantic Cache
        cached_res = self.cache.get(prompt, model_name)
        if cached_res:
            self.tracker.log_cache_hit(estimated_tokens=len(prompt.split()) + len(cached_res.split()))
            return cached_res

        # 2. Call Gemini API with resilient candidate fallbacks
        combined_prompt = f"{system_prompt}\n\n{prompt}"
        candidate_models = [
            "gemini-3.7-flash",
            "gemini-3.5-flash-lite",
            "gemini-3.5-flash",
            "gemini-3.8-flash",
            "gemini-flash-latest"
        ]
        
        output_text = ""
        resolved_model = model_name
        for m in candidate_models:
            try:
                response = self.gemini_client.models.generate_content(
                    model=m,
                    contents=combined_prompt
                )
                output_text = response.text or ""
                if output_text:
                    resolved_model = m
                    break
            except Exception:
                continue

        # 3. Track Token Usage & Estimated Costs
        input_tokens = len(combined_prompt.split()) * 2
        output_tokens = len(output_text.split()) * 2
        self.tracker.calculate_cost(
            model_name=resolved_model,
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )
        
        # 4. Save to Semantic Cache
        if output_text:
            self.cache.set(prompt, resolved_model, output_text)
        return output_text


