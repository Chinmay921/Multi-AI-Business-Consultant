"""Editor Agent: Synthesizes outputs into a polished client-ready report."""

from typing import Dict, Any
from src.schemas import FullReport
from src.utils.llm import get_llm
from src.utils.render import ReportRenderer
from src.utils.stitch import ReportStitcher


class EditorAgent:
    """Agent responsible for final report editing and synthesis."""
    
    def __init__(self):
        self.llm = get_llm()
        self.renderer = ReportRenderer()
        self.stitcher = ReportStitcher()
    
    def synthesize(self, report: FullReport) -> str:
        """
        Synthesize all agent outputs into a polished report.
        
        Args:
            report: FullReport with all sections
            
        Returns:
            Polished report text
        """
        system_prompt = """You are a professional business report editor. Your role is to:
1. Ensure consistency across all sections
2. Improve clarity and readability
3. Maintain professional tone
4. Ensure logical flow
5. Add executive summary insights

Create a client-ready, professional business report."""
        
        # Convert report to dict for rendering
        report_dict = report.model_dump()
        
        # Use renderer to create the full report
        report_text = self.renderer.render_full_report(report_dict)
        
        # Optionally, use LLM to polish the executive summary
        if report.executive_summary:
            polish_prompt = f"""Review and improve this executive summary for a business consulting report. 
Make it concise, clear, and impactful:

{report.executive_summary}

Provide an improved version that:
- Is clear and concise
- Highlights key insights
- Maintains professional tone
- Is suitable for C-level executives"""
            
            polished_summary = self.llm.generate(polish_prompt, system_prompt)
            report_dict['executive_summary'] = polished_summary
        
        # Re-render with polished summary
        final_report = self.renderer.render_full_report(report_dict)
        
        return final_report
    
    def create_report_sections(self, report: FullReport) -> Dict[str, str]:
        """
        Create individual report sections.
        
        Args:
            report: FullReport object
            
        Returns:
            Dictionary of section names to rendered content
        """
        report_dict = report.model_dump()
        sections = {}
        
        # Render each section
        if report.discovery:
            sections['discovery'] = self.renderer.render_section(
                'discovery',
                {'discovery': report_dict['discovery']}
            )
        
        if report.market_analysis:
            sections['market'] = self.renderer.render_section(
                'market',
                {'market_analysis': report_dict['market_analysis']}
            )
        
        if report.strategy:
            sections['strategy'] = self.renderer.render_section(
                'strategy',
                {'strategy': report_dict['strategy']}
            )
        
        if report.execution_plan:
            sections['execution'] = self.renderer.render_section(
                'execution',
                {'execution_plan': report_dict['execution_plan']}
            )
        
        if report.financial_model:
            sections['financial'] = self.renderer.render_section(
                'financial',
                {'financial_model': report_dict['financial_model']}
            )
        
        if report.risk_analysis:
            sections['risks'] = self.renderer.render_section(
                'risks',
                {'risk_analysis': report_dict['risk_analysis']}
            )
        
        return sections

