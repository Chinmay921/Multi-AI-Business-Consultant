"""Main entry point for the Multi-AI Business Consultant."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from src.schemas import ClientInput
from src.orchestrator import BusinessConsultantOrchestrator

# Load environment variables
load_dotenv()


def get_client_input() -> ClientInput:
    """
    Collect client input interactively.
    
    Returns:
        ClientInput object
    """
    print("=" * 60)
    print("Multi-AI Business Consultant")
    print("=" * 60)
    print("\nPlease provide the following information:\n")
    
    business = input("Business Description: ").strip()
    if not business:
        print("Error: Business description is required")
        sys.exit(1)
    
    industry = input("Industry: ").strip()
    if not industry:
        print("Error: Industry is required")
        sys.exit(1)
    
    goal = input("Primary Business Goal: ").strip()
    if not goal:
        print("Error: Business goal is required")
        sys.exit(1)
    
    constraints = input("Constraints (press Enter if none): ").strip()
    
    additional_context = input("Additional Context (press Enter if none): ").strip()
    
    return ClientInput(
        business=business,
        industry=industry,
        goal=goal,
        constraints=constraints if constraints else "None specified",
        additional_context=additional_context if additional_context else None
    )


def main():
    """Main execution function."""
    try:
        # Get client input
        client_input = get_client_input()
        
        print("\n" + "=" * 60)
        print("Generating Business Report...")
        print("=" * 60 + "\n")
        
        # Initialize orchestrator
        orchestrator = BusinessConsultantOrchestrator()
        
        # Generate report
        report = orchestrator.generate_report(client_input)
        
        # Save report
        output_dir = os.getenv("OUTPUT_DIR", "outputs")
        report_path = orchestrator.save_report(report, output_dir)
        
        print("\n" + "=" * 60)
        print("Report Generation Complete!")
        print("=" * 60)
        print(f"\nReport saved to: {report_path}")
        print(f"Report includes:")
        print(f"  - Executive Summary")
        print(f"  - Discovery Analysis")
        print(f"  - Market & Competitor Analysis")
        print(f"  - Strategic Recommendations")
        print(f"  - 30/60/90 Day Execution Plan")
        print(f"  - Financial Model & ROI Analysis")
        print(f"  - Risk Analysis & Mitigations")
        print(f"  - KPI Dashboard")
        print("\n")
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

