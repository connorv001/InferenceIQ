from typing import Tuple, List

class ModelRouter:
    """
    Intelligent router to select the most cost-effective model 
    based on prompt complexity.
    """
    
    COMPLEX_KEYWORDS = [
        "explain", "analyze", "summarize", "code", "debug", 
        "reason", "why", "how", "compare", "evaluate", "json",
        "script", "python"
    ]
    
    def __init__(self, length_threshold: int = 100):
        self.length_threshold = length_threshold

    def is_complex(self, prompt: str) -> bool:
        """
        Determine if a prompt is complex based on length and keywords.
        """
        prompt_lower = prompt.lower()
        
        # Rule 1: Length check
        if len(prompt) > self.length_threshold:
            return True
            
        # Rule 2: Keyword check
        if any(keyword in prompt_lower for keyword in self.COMPLEX_KEYWORDS):
            return True
            
        return False

    def route(self, prompt: str, strong_model: str, weak_model: str) -> Tuple[str, str]:
        """
        Returns (selected_model, reason).
        """
        if self.is_complex(prompt):
            return strong_model, "complexity_high"
        return weak_model, "complexity_low"
