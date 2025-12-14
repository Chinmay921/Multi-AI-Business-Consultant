"""Ops/Execution Agent: Creates execution plans and process improvements."""

from typing import Dict, Any
from src.schemas import (
    ClientInput,
    DiscoveryOutput,
    StrategyOutput,
    ExecutionPlan
)
from src.utils.llm import get_llm
from src.utils.json_parse import extract_json, validate_and_fix_json


class OpsAgent:
    """Agent responsible for operational planning and execution."""
    
    def __init__(self):
        self.llm = get_llm()
    
    def analyze(
        self,
        client_input: ClientInput,
        discovery: DiscoveryOutput,
        strategy: StrategyOutput
    ) -> ExecutionPlan:
        """
        Create execution plan with 30/60/90 day milestones.
        
        Args:
            client_input: Client input
            discovery: Discovery output
            strategy: Strategy output
            
        Returns:
            ExecutionPlan with detailed action items
        """
        system_prompt = """You are an operations and execution consultant. Your role is to:
1. Create actionable 30/60/90 day plans
2. Identify process improvements
3. Recommend organizational changes
4. Define resource requirements

Be specific and actionable in your recommendations."""
        
        prompt = f"""Create a detailed execution plan:

**Business**: {client_input.business}
**Recommended Strategy**: {strategy.recommendation}
**Rationale**: {strategy.rationale}
**Constraints**: {client_input.constraints}
**Success Metrics**: {', '.join(strategy.success_metrics)}

Please provide:
1. 30-day action plan with specific tasks
2. 60-day action plan with milestones
3. 90-day action plan with goals
4. Process improvements needed
5. Organizational changes required
6. Resource requirements (people, budget, tools)

Format your response as JSON:
{{
    "plan_30_days": [
        {{
            "task": "Task description",
            "owner": "Responsible party",
            "priority": "high/medium/low",
            "status": "not_started"
        }}
    ],
    "plan_60_days": [
        {{
            "task": "Task description",
            "owner": "Responsible party",
            "priority": "high/medium/low",
            "status": "not_started"
        }}
    ],
    "plan_90_days": [
        {{
            "task": "Task description",
            "owner": "Responsible party",
            "priority": "high/medium/low",
            "status": "not_started"
        }}
    ],
    "process_improvements": ["improvement1", "improvement2", ...],
    "org_changes": ["change1", "change2", ...],
    "resource_requirements": {{
        "people": "Description of staffing needs",
        "budget": "Budget estimate or description",
        "tools": ["tool1", "tool2", ...]
    }}
}}"""
        
        response = self.llm.generate(prompt, system_prompt, json_mode=True)
        data = extract_json(response)
        
        if not data:
            data = self._parse_fallback(strategy)
        
        try:
            return validate_and_fix_json(data, ExecutionPlan)
        except Exception as e:
            print(f"Error validating execution plan: {e}")
            return ExecutionPlan(
                plan_30_days=[],
                plan_60_days=[],
                plan_90_days=[],
                process_improvements=[],
                org_changes=[],
                resource_requirements={}
            )
    
    def _parse_fallback(self, strategy: StrategyOutput) -> Dict[str, Any]:
        """Fallback parser."""
        return {
            "plan_30_days": [
                {
                    "task": "Initiate strategy implementation",
                    "owner": "Leadership team",
                    "priority": "high",
                    "status": "not_started"
                }
            ],
            "plan_60_days": [
                {
                    "task": "Execute key initiatives",
                    "owner": "Operations team",
                    "priority": "high",
                    "status": "not_started"
                }
            ],
            "plan_90_days": [
                {
                    "task": "Review progress and adjust",
                    "owner": "Leadership team",
                    "priority": "medium",
                    "status": "not_started"
                }
            ],
            "process_improvements": ["Streamline operations", "Improve efficiency"],
            "org_changes": ["Align team structure with strategy"],
            "resource_requirements": {
                "people": "To be determined",
                "budget": "To be determined",
                "tools": []
            }
        }

