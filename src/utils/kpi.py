"""Utilities for generating KPI dashboards and metrics."""

from typing import Dict, Any, List, Optional
import json
from src.schemas import KPIMetrics, FinancialModel, StrategyOutput, ExecutionPlan


class KPIGenerator:
    """Generates KPI metrics and dashboards from agent outputs."""
    
    def __init__(self):
        self.metrics = {}
    
    def generate_from_agents(
        self,
        financial: Optional[FinancialModel] = None,
        strategy: Optional[StrategyOutput] = None,
        execution: Optional[ExecutionPlan] = None
    ) -> KPIMetrics:
        """
        Generate KPI metrics from agent outputs.
        
        Args:
            financial: Financial model output
            strategy: Strategy output
            execution: Execution plan output
            
        Returns:
            KPIMetrics object
        """
        revenue_metrics = {}
        operational_metrics = {}
        customer_metrics = {}
        financial_metrics = {}
        targets = {}
        
        # Extract from financial model
        if financial:
            if financial.unit_economics:
                revenue_metrics['unit_economics'] = financial.unit_economics
            if financial.revenue_projections:
                revenue_metrics['projections'] = financial.revenue_projections
            if financial.roi_model:
                financial_metrics['roi'] = financial.roi_model
            if financial.break_even_analysis:
                financial_metrics['break_even'] = financial.break_even_analysis
        
        # Extract from strategy
        if strategy:
            if strategy.success_metrics:
                targets['strategic_metrics'] = strategy.success_metrics
        
        # Extract from execution plan
        if execution:
            operational_metrics['milestones_30'] = len(execution.plan_30_days)
            operational_metrics['milestones_60'] = len(execution.plan_60_days)
            operational_metrics['milestones_90'] = len(execution.plan_90_days)
            if execution.resource_requirements:
                operational_metrics['resources'] = execution.resource_requirements
        
        return KPIMetrics(
            revenue_metrics=revenue_metrics,
            operational_metrics=operational_metrics,
            customer_metrics=customer_metrics,
            financial_metrics=financial_metrics,
            targets=targets
        )
    
    def create_dashboard_data(self, kpi: KPIMetrics) -> Dict[str, Any]:
        """
        Create dashboard data structure for visualization.
        
        Args:
            kpi: KPIMetrics object
            
        Returns:
            Dictionary suitable for dashboard rendering
        """
        return {
            'revenue': {
                'metrics': kpi.revenue_metrics,
                'chart_type': 'line',
                'title': 'Revenue Metrics'
            },
            'operations': {
                'metrics': kpi.operational_metrics,
                'chart_type': 'bar',
                'title': 'Operational Metrics'
            },
            'customers': {
                'metrics': kpi.customer_metrics,
                'chart_type': 'pie',
                'title': 'Customer Metrics'
            },
            'financial': {
                'metrics': kpi.financial_metrics,
                'chart_type': 'line',
                'title': 'Financial Metrics'
            },
            'targets': {
                'metrics': kpi.targets,
                'chart_type': 'gauge',
                'title': 'Target Metrics'
            }
        }
    
    def format_metrics_for_display(self, kpi: KPIMetrics) -> str:
        """
        Format KPI metrics as a readable string.
        
        Args:
            kpi: KPIMetrics object
            
        Returns:
            Formatted string representation
        """
        lines = ["# KPI Dashboard\n"]
        
        if kpi.revenue_metrics:
            lines.append("## Revenue Metrics")
            for key, value in kpi.revenue_metrics.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")
        
        if kpi.operational_metrics:
            lines.append("## Operational Metrics")
            for key, value in kpi.operational_metrics.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")
        
        if kpi.financial_metrics:
            lines.append("## Financial Metrics")
            for key, value in kpi.financial_metrics.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")
        
        if kpi.targets:
            lines.append("## Target Metrics")
            for key, value in kpi.targets.items():
                lines.append(f"- **{key}**: {value}")
        
        return "\n".join(lines)

