"""Utilities for rendering reports using Jinja2 templates."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from datetime import datetime


class ReportRenderer:
    """Renders business reports using Jinja2 templates."""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize the renderer.
        
        Args:
            template_dir: Directory containing Jinja2 templates. 
                         Defaults to templates/ relative to project root.
        """
        if template_dir is None:
            # Get project root (assuming this is in src/utils/)
            project_root = Path(__file__).parent.parent.parent
            template_dir = str(project_root / "templates")
        
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def render_template(
        self,
        template_name: str,
        context: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> str:
        """
        Render a template with the given context.
        
        Args:
            template_name: Name of the template file
            context: Dictionary of variables to pass to template
            output_path: Optional path to save rendered output
            
        Returns:
            Rendered string
        """
        try:
            template = self.env.get_template(template_name)
        except TemplateNotFound:
            # Try with .j2 extension if not provided
            if not template_name.endswith('.j2'):
                template_name = f"{template_name}.j2"
                template = self.env.get_template(template_name)
            else:
                raise
        
        rendered = template.render(**context)
        
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(rendered)
        
        return rendered
    
    def render_full_report(
        self,
        report_data: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> str:
        """
        Render the complete business report.
        
        Args:
            report_data: Dictionary containing all report sections
            output_path: Optional path to save the report
            
        Returns:
            Rendered full report
        """
        # Add metadata
        context = {
            **report_data,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': '1.0'
        }
        
        return self.render_template('full_report.md.j2', context, output_path)
    
    def render_section(
        self,
        section_name: str,
        section_data: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> str:
        """
        Render a specific section of the report.
        
        Args:
            section_name: Name of the section template
            section_data: Data for the section
            output_path: Optional path to save the section
            
        Returns:
            Rendered section
        """
        template_map = {
            'executive_summary': 'executive_summary.md.j2',
            'market': 'market_competitors.md.j2',
            'strategy': 'strategy_recommendation.md.j2',
            'execution': 'plan_30_60_90.md.j2',
            'financial': 'financial_model.md.j2',
            'risks': 'risks.md.j2'
        }
        
        template_name = template_map.get(section_name, f"{section_name}.md.j2")
        return self.render_template(template_name, section_data, output_path)

