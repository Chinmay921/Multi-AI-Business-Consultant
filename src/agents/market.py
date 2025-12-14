"""Market/Competitor Agent: Analyzes market and competitors."""

from typing import Dict, Any
from src.schemas import ClientInput, DiscoveryOutput, MarketAnalysis
from src.utils.llm import get_llm
from src.utils.json_parse import extract_json, validate_and_fix_json


class MarketAgent:
    """Agent responsible for market and competitor analysis."""
    
    def __init__(self):
        self.llm = get_llm()
    
    def analyze(
        self,
        client_input: ClientInput,
        discovery: DiscoveryOutput
    ) -> MarketAnalysis:
        """
        Analyze market and competitors.
        
        Args:
            client_input: Client input
            discovery: Discovery agent output
            
        Returns:
            MarketAnalysis with competitor map and positioning
        """
        system_prompt = """You are a market research and competitive intelligence expert. Your role is to:
1. Identify key competitors
2. Create a competitor map
3. Find differentiation opportunities
4. Recommend positioning strategies
5. Analyze market size and trends

Provide actionable insights based on the business context."""
        
        prompt = f"""Conduct a comprehensive market and competitor analysis:

**Business**: {client_input.business}
**Industry**: {client_input.industry}
**Target Market**: {discovery.target_market}
**Business Model**: {discovery.business_model}

Please provide:
1. List of key competitors with their strengths/weaknesses
2. A competitor positioning map
3. Differentiation opportunities
4. Recommended positioning strategy
5. Market size estimate (if possible)
6. Key market trends

Format your response as JSON:
{{
    "competitors": [
        {{
            "name": "Competitor Name",
            "strengths": ["strength1", "strength2"],
            "weaknesses": ["weakness1", "weakness2"],
            "market_position": "description"
        }}
    ],
    "competitor_map": {{
        "dimensions": ["dimension1", "dimension2"],
        "positions": {{"competitor_name": [x, y]}}
    }},
    "differentiation_opportunities": ["opportunity1", "opportunity2", ...],
    "positioning_strategy": "Recommended positioning strategy",
    "market_size": "Market size estimate or description",
    "market_trends": ["trend1", "trend2", ...]
}}"""
        
        response = self.llm.generate(prompt, system_prompt, json_mode=True)
        data = extract_json(response)
        
        if not data:
            data = self._parse_fallback(client_input, discovery)
        
        try:
            return validate_and_fix_json(data, MarketAnalysis)
        except Exception as e:
            print(f"Error validating market analysis: {e}")
            return MarketAnalysis(
                competitors=[],
                competitor_map={},
                differentiation_opportunities=[],
                positioning_strategy="To be developed based on market research"
            )
    
    def _parse_fallback(
        self,
        client_input: ClientInput,
        discovery: DiscoveryOutput
    ) -> Dict[str, Any]:
        """Fallback parser."""
        return {
            "competitors": [],
            "competitor_map": {},
            "differentiation_opportunities": [
                f"Focus on {client_input.industry} expertise",
                "Leverage unique business model"
            ],
            "positioning_strategy": f"Position as a {discovery.business_model} in {client_input.industry}",
            "market_size": "To be researched",
            "market_trends": []
        }

