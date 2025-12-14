"""Risk/Legal Agent: Identifies risks and compliance issues."""

from typing import Dict, Any
from src.schemas import (
    ClientInput,
    DiscoveryOutput,
    StrategyOutput,
    RiskAnalysis
)
from src.utils.llm import get_llm
from src.utils.json_parse import extract_json, validate_and_fix_json


class RiskAgent:
    """Agent responsible for risk assessment and compliance."""
    
    def __init__(self):
        self.llm = get_llm()
    
    def analyze(
        self,
        client_input: ClientInput,
        discovery: DiscoveryOutput,
        strategy: StrategyOutput
    ) -> RiskAnalysis:
        """
        Identify risks, mitigations, and compliance issues.
        
        Args:
            client_input: Client input
            discovery: Discovery output
            strategy: Strategy output
            
        Returns:
            RiskAnalysis with risks and mitigations
        """
        system_prompt = """You are a risk management and legal compliance consultant. Your role is to:
1. Identify business risks
2. Recommend mitigation strategies
3. Flag compliance issues
4. Highlight legal considerations

Be thorough and consider both obvious and hidden risks."""
        
        prompt = f"""Conduct a comprehensive risk analysis:

**Business**: {client_input.business}
**Industry**: {client_input.industry}
**Strategy**: {strategy.recommendation}
**Constraints**: {client_input.constraints}
**Business Model**: {discovery.business_model}

Please provide:
1. List of key risks with severity and likelihood
2. Mitigation strategies for each risk
3. Compliance flags specific to the industry
4. Legal considerations

Format your response as JSON:
{{
    "risks": [
        {{
            "category": "Financial/Operational/Legal/Strategic",
            "description": "Risk description",
            "severity": "high/medium/low",
            "likelihood": "high/medium/low",
            "impact": "Impact description"
        }}
    ],
    "mitigations": [
        {{
            "risk_id": "Reference to risk",
            "strategy": "Mitigation strategy",
            "owner": "Responsible party",
            "timeline": "When to implement"
        }}
    ],
    "compliance_flags": ["flag1", "flag2", ...],
    "legal_considerations": ["consideration1", "consideration2", ...]
}}"""
        
        response = self.llm.generate(prompt, system_prompt, json_mode=True)
        data = extract_json(response)
        
        if not data:
            data = self._parse_fallback(client_input, strategy)
        
        try:
            return validate_and_fix_json(data, RiskAnalysis)
        except Exception as e:
            print(f"Error validating risk analysis: {e}")
            return RiskAnalysis(
                risks=[],
                mitigations=[],
                compliance_flags=[],
                legal_considerations=[]
            )
    
    def _parse_fallback(
        self,
        client_input: ClientInput,
        strategy: StrategyOutput
    ) -> Dict[str, Any]:
        """Fallback parser."""
        return {
            "risks": [
                {
                    "category": "Strategic",
                    "description": "Strategy execution risk",
                    "severity": "medium",
                    "likelihood": "medium",
                    "impact": "May affect goal achievement"
                }
            ],
            "mitigations": [
                {
                    "risk_id": "Strategy execution risk",
                    "strategy": "Regular monitoring and adjustment",
                    "owner": "Leadership team",
                    "timeline": "Ongoing"
                }
            ],
            "compliance_flags": [
                f"Industry-specific regulations for {client_input.industry}",
                "Data privacy and security requirements"
            ],
            "legal_considerations": [
                "Contractual obligations",
                "Regulatory compliance",
                "Intellectual property protection"
            ]
        }

