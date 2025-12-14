"""Discovery Agent: Clarifies problems, assumptions, and gathers facts."""

from typing import Dict, Any
from src.schemas import ClientInput, DiscoveryOutput
from src.utils.llm import get_llm
from src.utils.json_parse import extract_json, validate_and_fix_json


class DiscoveryAgent:
    """Agent responsible for discovery and problem clarification."""
    
    def __init__(self):
        self.llm = get_llm()
    
    def analyze(self, client_input: ClientInput) -> DiscoveryOutput:
        """
        Analyze client input and gather additional information.
        
        Args:
            client_input: Initial client input
            
        Returns:
            DiscoveryOutput with problem statement, assumptions, and facts
        """
        system_prompt = """You are a business discovery consultant. Your role is to:
1. Clarify the problem statement
2. Identify key assumptions
3. Gather relevant facts
4. Understand the business model
5. Identify the target market

Respond in a structured format that helps understand the client's situation."""
        
        prompt = f"""Analyze the following client information and provide a comprehensive discovery analysis:

**Business**: {client_input.business}
**Industry**: {client_input.industry}
**Goal**: {client_input.goal}
**Constraints**: {client_input.constraints}
{f"**Additional Context**: {client_input.additional_context}" if client_input.additional_context else ""}

Please provide:
1. A clear problem statement
2. Key assumptions that need validation
3. Facts gathered from the information
4. Questions that need clarification
5. Business model description
6. Target market identification

Format your response as JSON with the following structure:
{{
    "problem_statement": "Clear statement of the problem",
    "key_assumptions": ["assumption1", "assumption2", ...],
    "facts_gathered": ["fact1", "fact2", ...],
    "questions_clarified": ["question1", "question2", ...],
    "business_model": "Description of how the business works",
    "target_market": "Description of target market"
}}"""
        
        response = self.llm.generate(prompt, system_prompt, json_mode=True)
        data = extract_json(response)
        
        if not data:
            # Fallback to structured text parsing
            data = self._parse_fallback(response)
        
        try:
            return validate_and_fix_json(data, DiscoveryOutput)
        except Exception as e:
            print(f"Error validating discovery output: {e}")
            # Return minimal valid output
            return DiscoveryOutput(
                problem_statement=client_input.goal,
                key_assumptions=[],
                facts_gathered=[client_input.business, client_input.industry],
                questions_clarified=[],
                business_model=client_input.business,
                target_market="To be determined"
            )
    
    def _parse_fallback(self, text: str) -> Dict[str, Any]:
        """Fallback parser if JSON extraction fails."""
        return {
            "problem_statement": text[:200] if text else "Problem to be clarified",
            "key_assumptions": [],
            "facts_gathered": [text] if text else [],
            "questions_clarified": [],
            "business_model": "To be determined",
            "target_market": "To be determined"
        }

