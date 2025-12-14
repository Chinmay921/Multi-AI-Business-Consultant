"""Utilities for stitching together agent outputs into a cohesive report."""

from typing import Dict, Any, List
from datetime import datetime
from src.schemas import (
    FullReport,
    DiscoveryOutput,
    MarketAnalysis,
    StrategyOutput,
    ExecutionPlan,
    FinancialModel,
    RiskAnalysis,
    KPIMetrics
)


class ReportStitcher:
    """Stitches together outputs from multiple agents into a unified report."""
    
    def __init__(self):
        self.sections = {}
    
    def add_discovery(self, discovery: DiscoveryOutput):
        """Add discovery agent output."""
        self.sections['discovery'] = discovery
    
    def add_market_analysis(self, market: MarketAnalysis):
        """Add market analysis output."""
        self.sections['market_analysis'] = market
    
    def add_strategy(self, strategy: StrategyOutput):
        """Add strategy agent output."""
        self.sections['strategy'] = strategy
    
    def add_execution_plan(self, execution: ExecutionPlan):
        """Add execution plan output."""
        self.sections['execution_plan'] = execution
    
    def add_financial_model(self, financial: FinancialModel):
        """Add financial model output."""
        self.sections['financial_model'] = financial
    
    def add_risk_analysis(self, risk: RiskAnalysis):
        """Add risk analysis output."""
        self.sections['risk_analysis'] = risk
    
    def add_kpi_metrics(self, kpi: KPIMetrics):
        """Add KPI metrics."""
        self.sections['kpi_dashboard'] = kpi
    
    def generate_executive_summary(self) -> str:
        """
        Generate executive summary from all sections.
        
        Returns:
            Executive summary text
        """
        summary_parts = []
        
        # Problem statement
        if 'discovery' in self.sections:
            discovery = self.sections['discovery']
            summary_parts.append(f"**Problem Statement**: {discovery.problem_statement}")
        
        # Key recommendation
        if 'strategy' in self.sections:
            strategy = self.sections['strategy']
            summary_parts.append(f"**Strategic Recommendation**: {strategy.recommendation}")
        
        # Financial highlights
        if 'financial_model' in self.sections:
            financial = self.sections['financial_model']
            if 'roi_model' in financial.roi_model:
                roi = financial.roi_model.get('roi', 'N/A')
                summary_parts.append(f"**Expected ROI**: {roi}")
        
        # Key risks
        if 'risk_analysis' in self.sections:
            risk = self.sections['risk_analysis']
            if risk.risks:
                top_risk = risk.risks[0]
                summary_parts.append(f"**Primary Risk**: {top_risk.get('description', 'N/A')}")
        
        return "\n\n".join(summary_parts)
    
    def build_full_report(self) -> FullReport:
        """
        Build the complete FullReport object.
        
        Returns:
            Complete FullReport with all sections
        """
        executive_summary = self.generate_executive_summary()
        
        return FullReport(
            executive_summary=executive_summary,
            discovery=self.sections.get('discovery'),
            market_analysis=self.sections.get('market_analysis'),
            strategy=self.sections.get('strategy'),
            execution_plan=self.sections.get('execution_plan'),
            financial_model=self.sections.get('financial_model'),
            risk_analysis=self.sections.get('risk_analysis'),
            kpi_dashboard=self.sections.get('kpi_dashboard')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the stitched report to a dictionary for rendering.
        
        Returns:
            Dictionary representation of the report
        """
        report = self.build_full_report()
        
        return {
            'executive_summary': report.executive_summary,
            'discovery': report.discovery.model_dump() if report.discovery else {},
            'market_analysis': report.market_analysis.model_dump() if report.market_analysis else {},
            'strategy': report.strategy.model_dump() if report.strategy else {},
            'execution_plan': report.execution_plan.model_dump() if report.execution_plan else {},
            'financial_model': report.financial_model.model_dump() if report.financial_model else {},
            'risk_analysis': report.risk_analysis.model_dump() if report.risk_analysis else {},
            'kpi_dashboard': report.kpi_dashboard.model_dump() if report.kpi_dashboard else {},
            'generated_at': report.generated_at.isoformat()
        }

