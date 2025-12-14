# Multi-AI Business Consultant

A comprehensive business consulting system powered by Qwen3:8b that generates detailed business reports, action plans, and KPI dashboards.

## Overview

This system uses multiple specialized AI agents to analyze a client's business, industry, goals, and constraints, then produces a comprehensive 10-15 page report with actionable recommendations.

## Architecture

### Agents

1. **Discovery Agent**: Clarifies problems, assumptions, and gathers facts from the user
2. **Market/Competitor Agent**: Creates competitor maps, identifies differentiation opportunities, and positioning strategies
3. **Strategy Agent**: Develops strategic options, analyzes tradeoffs, and provides recommendations
4. **Ops/Execution Agent**: Creates 30/60/90 day plans, process improvements, and organizational changes
5. **Finance Agent**: Builds unit economics, pricing models, and ROI calculations
6. **Risk/Legal Agent**: Identifies risks, mitigations, and compliance flags
7. **Editor Agent**: Synthesizes all outputs into a polished client-ready report

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with the following configuration:
```bash
# Ollama Configuration (Recommended for local qwen3:8b)
USE_OLLAMA=true
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=qwen3:8b

# Alternative: External API Configuration
# USE_OLLAMA=false
# QWEN_API_KEY=your_api_key_here
# QWEN_API_BASE=https://api.example.com/v1

# Model Configuration
TEMPERATURE=0.7
MAX_TOKENS=4000

# Output Configuration
OUTPUT_DIR=outputs
LOG_LEVEL=INFO
```

**Note:** Make sure Ollama is running before using the system:
```bash
# Check if Ollama is running
ollama list

# If not running, start Ollama (usually runs automatically)
# ollama serve
```

## Usage

Run from the project root:

```bash
python main.py
```

Or run as a module:

```bash
python -m src.main
```

Or if you've installed the package:

```bash
business-consultant
```

The system will prompt you for:
- Client business description
- Industry
- Goals
- Constraints

Output will be generated in the `outputs/` directory.

## Project Structure

```
multi-ai-business-consultant/
├── README.md
├── requirements.txt
├── .env.example
├── src/
│   ├── main.py
│   ├── orchestrator.py
│   ├── schemas.py
│   ├── agents/
│   │   ├── discovery.py
│   │   ├── market.py
│   │   ├── strategy.py
│   │   ├── ops.py
│   │   ├── finance.py
│   │   ├── risk.py
│   │   └── editor.py
│   └── utils/
│       ├── llm.py
│       ├── json_parse.py
│       ├── render.py
│       ├── stitch.py
│       └── kpi.py
├── templates/
│   ├── executive_summary.md.j2
│   ├── market_competitors.md.j2
│   ├── strategy_recommendation.md.j2
│   ├── plan_30_60_90.md.j2
│   ├── financial_model.md.j2
│   ├── risks.md.j2
│   └── full_report.md.j2
└── outputs/
```

## Output

The system generates:
- A comprehensive business report
- Action plan with 30/60/90 day milestones
- KPI dashboard with key metrics

All outputs are saved in the `outputs/` directory with timestamps.

## Implementation Notes

### LLM Integration

The `src/utils/llm.py` module supports Ollama for local model inference:

- **Ollama (Recommended)**: Uses your local `qwen3:8b` model via Ollama's API
  - Set `USE_OLLAMA=true` in `.env`
  - Ensure Ollama is running (`ollama serve` or it runs automatically)
  - The system will connect to `http://localhost:11434` by default
  
- **External API**: If Qwen3:8b is available via an OpenAI-compatible API:
  - Set `USE_OLLAMA=false`
  - Configure `QWEN_API_KEY` and `QWEN_API_BASE`

### Customization

- **Templates**: Modify Jinja2 templates in `templates/` to customize report formatting
- **Agents**: Each agent can be customized in `src/agents/` to adjust analysis depth and focus
- **Schemas**: Update `src/schemas.py` to modify data structures and validation rules

