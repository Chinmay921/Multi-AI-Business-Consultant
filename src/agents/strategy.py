"""Strategy Agent: Develops strategic options and recommendations."""

from typing import Dict, Any
from src.schemas import ClientInput, DiscoveryOutput, MarketAnalysis, StrategyOutput
from src.utils.llm import get_llm
from src.utils.json_parse import extract_json, validate_and_fix_json


class StrategyAgent:
    """Agent responsible for strategic planning and recommendations."""
    
    def __init__(self):
        self.llm = get_llm()
    
    def analyze(
        self,
        client_input: ClientInput,
        discovery: DiscoveryOutput,
        market: MarketAnalysis
    ) -> StrategyOutput:
        """
        Develop strategic options and recommendations.
        
        Args:
            client_input: Client input
            discovery: Discovery output
            market: Market analysis
            
        Returns:
            StrategyOutput with options, tradeoffs, and recommendation
        """
        system_prompt = """You are a strategic business consultant. Your role is to:
1. Develop multiple strategic options
2. Analyze tradeoffs between options
3. Provide a clear recommendation
4. Explain the rationale
5. Define success metrics

Think strategically and consider long-term implications."""
        
        prompt = f"""Develop strategic recommendations:

**Business Goal**: {client_input.goal}
**Problem Statement**: {discovery.problem_statement}
**Constraints**: {client_input.constraints}
**Market Position**: {market.positioning_strategy}
**Differentiation Opportunities**: {', '.join(market.differentiation_opportunities[:3])}

Please provide:
1. 3-5 strategic options with descriptions
2. Tradeoffs analysis for each option
3. A clear recommendation
4. Rationale for the recommendation
5. Success metrics to track

Format your response as JSON:
{{
    "strategic_options": [
        {{
            "name": "Option Name",
            "description": "Detailed description",
            "pros": ["pro1", "pro2"],
            "cons": ["con1", "con2"],
            "feasibility": "high/medium/low",
            "impact": "high/medium/low"
        }}
    ],
    "tradeoffs": {{
        "option1_vs_option2": "Comparison description",
        "risk_vs_reward": "Analysis"
    }},
    "recommendation": "Recommended strategic option with justification",
    "rationale": "Detailed rationale for the recommendation",
    "success_metrics": ["metric1", "metric2", ...]
}}"""
        
        response = self.llm.generate(prompt, system_prompt, json_mode=True)
        data = extract_json(response)
        
        if not data:
            data = self._parse_fallback(client_input, discovery)
        
        try:
            return validate_and_fix_json(data, StrategyOutput)
        except Exception as e:
            print(f"Error validating strategy output: {e}")
            return StrategyOutput(
                strategic_options=[],
                tradeoffs={},
                recommendation=f"Focus on achieving {client_input.goal} while addressing {discovery.problem_statement}",
                rationale="Based on business context and constraints",
                success_metrics=["Revenue growth", "Market share", "Customer satisfaction"]
            )
    
    def _parse_fallback(
        self,
        client_input: ClientInput,
        discovery: DiscoveryOutput
    ) -> Dict[str, Any]:
        """Fallback parser."""
        return {
            "strategic_options": [
                {
                    "name": "Primary Strategy",
                    "description": f"Focus on {client_input.goal}",
                    "pros": ["Aligned with goals"],
                    "cons": ["Requires resources"],
                    "feasibility": "medium",
                    "impact": "high"
                }
            ],
            "tradeoffs": {},
            "recommendation": f"Implement strategy to achieve {client_input.goal}",
            "rationale": f"Addresses {discovery.problem_statement}",
            "success_metrics": ["Goal achievement", "Progress tracking"]
        }

