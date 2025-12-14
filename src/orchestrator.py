"""Orchestrator: Coordinates all agents to generate the business report."""

from typing import Optional
from src.schemas import ClientInput, FullReport
from src.agents.discovery import DiscoveryAgent
from src.agents.market import MarketAgent
from src.agents.strategy import StrategyAgent
from src.agents.ops import OpsAgent
from src.agents.finance import FinanceAgent
from src.agents.risk import RiskAgent
from src.agents.editor import EditorAgent
from src.utils.stitch import ReportStitcher
from src.utils.kpi import KPIGenerator


class BusinessConsultantOrchestrator:
    """Orchestrates the multi-agent business consulting process."""
    
    def __init__(self):
        self.discovery_agent = DiscoveryAgent()
        self.market_agent = MarketAgent()
        self.strategy_agent = StrategyAgent()
        self.ops_agent = OpsAgent()
        self.finance_agent = FinanceAgent()
        self.risk_agent = RiskAgent()
        self.editor_agent = EditorAgent()
        self.stitcher = ReportStitcher()
        self.kpi_generator = KPIGenerator()
    
    def generate_report(self, client_input: ClientInput) -> FullReport:
        """
        Generate a complete business consulting report.
        
        Args:
            client_input: Client input with business information
            
        Returns:
            Complete FullReport with all sections
        """
        print("🔍 Starting Discovery Phase...")
        discovery = self.discovery_agent.analyze(client_input)
        self.stitcher.add_discovery(discovery)
        print("✓ Discovery complete")
        
        print("\n📊 Starting Market Analysis...")
        market = self.market_agent.analyze(client_input, discovery)
        self.stitcher.add_market_analysis(market)
        print("✓ Market analysis complete")
        
        print("\n🎯 Starting Strategy Development...")
        strategy = self.strategy_agent.analyze(client_input, discovery, market)
        self.stitcher.add_strategy(strategy)
        print("✓ Strategy development complete")
        
        print("\n⚙️  Starting Operations Planning...")
        execution = self.ops_agent.analyze(client_input, discovery, strategy)
        self.stitcher.add_execution_plan(execution)
        print("✓ Operations planning complete")
        
        print("\n💰 Starting Financial Modeling...")
        financial = self.finance_agent.analyze(client_input, discovery, strategy)
        self.stitcher.add_financial_model(financial)
        print("✓ Financial modeling complete")
        
        print("\n⚠️  Starting Risk Analysis...")
        risk = self.risk_agent.analyze(client_input, discovery, strategy)
        self.stitcher.add_risk_analysis(risk)
        print("✓ Risk analysis complete")
        
        print("\n📈 Generating KPI Dashboard...")
        kpi = self.kpi_generator.generate_from_agents(financial, strategy, execution)
        self.stitcher.add_kpi_metrics(kpi)
        print("✓ KPI dashboard complete")
        
        print("\n📝 Synthesizing Final Report...")
        full_report = self.stitcher.build_full_report()
        print("✓ Report synthesis complete")
        
        return full_report
    
    def save_report(
        self,
        report: FullReport,
        output_dir: str = "outputs",
        filename: Optional[str] = None
    ) -> str:
        """
        Save the report to disk.
        
        Args:
            report: FullReport to save
            output_dir: Output directory
            filename: Optional custom filename
            
        Returns:
            Path to saved report
        """
        import os
        from datetime import datetime
        
        os.makedirs(output_dir, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"business_report_{timestamp}.md"
        
        output_path = os.path.join(output_dir, filename)
        
        # Render and save the report
        report_dict = self.stitcher.to_dict()
        self.editor_agent.renderer.render_full_report(report_dict, output_path)
        
        print(f"\n✅ Report saved to: {output_path}")
        return output_path

