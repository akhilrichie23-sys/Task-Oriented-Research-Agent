import tiktoken

class CostTracker:
    # Pricing per 1k tokens (Gemini models)
    PRICING = {
        "gemini-3.7-flash": {"input": 0.000075, "output": 0.0003},
        "gemini-3.5-flash": {"input": 0.000075, "output": 0.0003},
        "gemini-3.5-flash-lite": {"input": 0.0000375, "output": 0.00015},
        "gemini-2.5-flash": {"input": 0.000075, "output": 0.0003},
        "gemini-2.5-flash-lite": {"input": 0.0000375, "output": 0.00015},
        "gemini-2.5-pro": {"input": 0.00125, "output": 0.005},
        "gemini-flash-latest": {"input": 0.000075, "output": 0.0003},
    }


    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.tokens_saved_by_cache = 0

    def calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> float:
        default_rate = self.PRICING.get("gemini-2.5-flash", {"input": 0.000075, "output": 0.0003})
        rates = self.PRICING.get(model_name, default_rate)
        input_cost = (input_tokens / 1000) * rates["input"]
        output_cost = (output_tokens / 1000) * rates["output"]
        cost = input_cost + output_cost

        
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost += cost
        return cost

    def log_cache_hit(self, estimated_tokens: int):
        self.tokens_saved_by_cache += estimated_tokens

    def get_summary(self) -> dict:
        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "estimated_cost_usd": round(self.total_cost, 6),
            "tokens_saved_via_cache": self.tokens_saved_by_cache,
        }
