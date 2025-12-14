"""Data schemas for the business consultant system."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ClientInput(BaseModel):
    """Initial client input."""
    business: str = Field(..., description="Description of the client's business")
    industry: str = Field(..., description="Industry sector")
    goal: str = Field(..., description="Primary business goal")
    constraints: str = Field(..., description="Business constraints and limitations")
    additional_context: Optional[str] = Field(None, description="Any additional context")


class DiscoveryOutput(BaseModel):
    """Output from Discovery Agent."""
    problem_statement: str
    key_assumptions: List[str]
    facts_gathered: List[str]
    questions_clarified: List[str]
    business_model: str
    target_market: str


class MarketAnalysis(BaseModel):
    """Output from Market/Competitor Agent."""
    competitors: List[Dict[str, Any]]
    competitor_map: Dict[str, Any]
    differentiation_opportunities: List[str]
    positioning_strategy: str
    market_size: Optional[str] = None
    market_trends: List[str] = []


class StrategyOutput(BaseModel):
    """Output from Strategy Agent."""
    strategic_options: List[Dict[str, Any]]
    tradeoffs: Dict[str, Any]
    recommendation: str
    rationale: str
    success_metrics: List[str]


class ExecutionPlan(BaseModel):
    """Output from Ops/Execution Agent."""
    plan_30_days: List[Dict[str, str]]
    plan_60_days: List[Dict[str, str]]
    plan_90_days: List[Dict[str, str]]
    process_improvements: List[str]
    org_changes: List[str]
    resource_requirements: Dict[str, Any]


class FinancialModel(BaseModel):
    """Output from Finance Agent."""
    unit_economics: Dict[str, Any]
    pricing_strategy: str
    revenue_projections: Dict[str, Any]
    cost_structure: Dict[str, Any]
    roi_model: Dict[str, Any]
    break_even_analysis: Dict[str, Any]


class RiskAnalysis(BaseModel):
    """Output from Risk/Legal Agent."""
    risks: List[Dict[str, Any]]
    mitigations: List[Dict[str, Any]]
    compliance_flags: List[str]
    legal_considerations: List[str]


class KPIMetrics(BaseModel):
    """KPI metrics for dashboard."""
    revenue_metrics: Dict[str, Any]
    operational_metrics: Dict[str, Any]
    customer_metrics: Dict[str, Any]
    financial_metrics: Dict[str, Any]
    targets: Dict[str, Any]


class FullReport(BaseModel):
    """Complete business consultant report."""
    executive_summary: str
    discovery: DiscoveryOutput
    market_analysis: MarketAnalysis
    strategy: StrategyOutput
    execution_plan: ExecutionPlan
    financial_model: FinancialModel
    risk_analysis: RiskAnalysis
    kpi_dashboard: KPIMetrics
    generated_at: datetime = Field(default_factory=datetime.now)

