"""Finance Agent: Builds financial models and unit economics."""

from typing import Dict, Any
from src.schemas import (
    ClientInput,
    DiscoveryOutput,
    StrategyOutput,
    FinancialModel
)
from src.utils.llm import get_llm
from src.utils.json_parse import extract_json, validate_and_fix_json


class FinanceAgent:
    """Agent responsible for financial modeling and analysis."""
    
    def __init__(self):
        self.llm = get_llm()
    
    def analyze(
        self,
        client_input: ClientInput,
        discovery: DiscoveryOutput,
        strategy: StrategyOutput
    ) -> FinancialModel:
        """
        Build financial model with unit economics and ROI.
        
        Args:
            client_input: Client input
            discovery: Discovery output
            strategy: Strategy output
            
        Returns:
            FinancialModel with economics and projections
        """
        system_prompt = """You are a financial modeling consultant. Your role is to:
1. Build unit economics models
2. Develop pricing strategies
3. Create revenue projections
4. Analyze cost structures
5. Calculate ROI and break-even points

Even if data is limited, provide reasonable estimates and assumptions."""
        
        prompt = f"""Build a financial model:

**Business**: {client_input.business}
**Business Model**: {discovery.business_model}
**Target Market**: {discovery.target_market}
**Strategy**: {strategy.recommendation}
**Constraints**: {client_input.constraints}

Please provide:
1. Unit economics (CAC, LTV, margins, etc.)
2. Pricing strategy recommendations
3. Revenue projections (monthly/quarterly/annual)
4. Cost structure breakdown
5. ROI model with assumptions
6. Break-even analysis

Format your response as JSON:
{{
    "unit_economics": {{
        "customer_acquisition_cost": "CAC estimate or description",
        "lifetime_value": "LTV estimate or description",
        "gross_margin": "Margin percentage or description",
        "contribution_margin": "Margin description"
    }},
    "pricing_strategy": "Recommended pricing approach",
    "revenue_projections": {{
        "month_1": "Revenue estimate",
        "month_3": "Revenue estimate",
        "month_6": "Revenue estimate",
        "year_1": "Revenue estimate"
    }},
    "cost_structure": {{
        "fixed_costs": "Description of fixed costs",
        "variable_costs": "Description of variable costs",
        "cost_breakdown": "Detailed breakdown"
    }},
    "roi_model": {{
        "investment": "Required investment",
        "expected_return": "Expected return",
        "roi": "ROI percentage or description",
        "payback_period": "Payback period estimate",
        "assumptions": ["assumption1", "assumption2"]
    }},
    "break_even_analysis": {{
        "break_even_point": "Break-even point description",
        "break_even_timeline": "Timeline to break even",
        "key_assumptions": ["assumption1", "assumption2"]
    }}
}}"""
        
        response = self.llm.generate(prompt, system_prompt, json_mode=True)
        data = extract_json(response)
        
        if not data:
            data = self._parse_fallback()
        
        try:
            return validate_and_fix_json(data, FinancialModel)
        except Exception as e:
            print(f"Error validating financial model: {e}")
            return FinancialModel(
                unit_economics={},
                pricing_strategy="To be determined based on market research",
                revenue_projections={},
                cost_structure={},
                roi_model={},
                break_even_analysis={}
            )
    
    def _parse_fallback(self) -> Dict[str, Any]:
        """Fallback parser."""
        return {
            "unit_economics": {
                "customer_acquisition_cost": "To be calculated",
                "lifetime_value": "To be calculated",
                "gross_margin": "To be determined",
                "contribution_margin": "To be determined"
            },
            "pricing_strategy": "Competitive pricing based on market analysis",
            "revenue_projections": {
                "month_1": "Initial revenue",
                "month_3": "Growing revenue",
                "month_6": "Established revenue",
                "year_1": "Annual revenue projection"
            },
            "cost_structure": {
                "fixed_costs": "Operational overhead",
                "variable_costs": "Cost of goods/services",
                "cost_breakdown": "To be detailed"
            },
            "roi_model": {
                "investment": "To be calculated",
                "expected_return": "To be projected",
                "roi": "To be calculated",
                "payback_period": "To be determined",
                "assumptions": ["Market conditions", "Execution success"]
            },
            "break_even_analysis": {
                "break_even_point": "To be calculated",
                "break_even_timeline": "To be determined",
                "key_assumptions": ["Revenue growth", "Cost management"]
            }
        }

