<div style="text-align: right;">
  <a href="README.md">English</a> | <a href="README.pt.md">Português</a>
</div>

# Performance Analytics Multi-Agent System

A multi-agent system that answers performance analytics questions by routing them to a specialized domain agent, running deterministic calculations, and synthesizing the results into a plain-language insight.

This is a learning project exploring how LLMs can be orchestrated reliably — using rules-based logic where possible and LLM reasoning only where it's actually needed.

## The problem

Performance analytics questions span very different domains — financial health, operational throughput, team productivity, product adoption, growth metrics — and each domain has its own formulas, data shapes, and ways of being misread.

A single general-purpose assistant tends to blur these together: it might apply financial intuition to a product question, or skip the actual math in favor of a plausible-sounding guess. The result is answers that sound confident but aren't grounded in real calculation.

This project takes a different approach: separate the *understanding* of a question from the *math* behind it, and separate the *math* from the *interpretation* of what it means.

## How it works

A query goes through three stages:

1. **Ingestion agent** — reads the query and figures out two things: which analytics track it belongs to, and whether any optional enrichment (like clustering) is being asked for. This uses a fast rules-based keyword check first, and only calls an LLM classifier if the query is ambiguous.
2. **Track agent** — receives the routed query and the relevant data, and calls **pre-built, deterministic Python functions** to do the actual math. No LLM is involved in calculating a margin or a churn rate — these are plain functions with predictable, auditable output.
3. **Synthesis agent** — takes the raw numbers (and any enrichment output) and turns them into an actual insight: not just "margin is 23%" but what that number means in context.

An orchestrator sits between steps 2 and 3, dispatching to the right track agent and optionally calling a clustering utility if the query asked for segmentation.

The whole pipeline is wrapped in a **Streamlit app** as the frontend — a simple interface for typing a query, supplying or uploading data, and viewing the synthesized insight (plus any cluster visualizations when enrichment runs).

```
User query
    │
    ▼
Ingestion agent  ──── rules-based filter → LLM fallback if ambiguous
    │
    ▼
Orchestrator ──── routes to one of 5 tracks
    │
    ▼
Track agent ──── calls deterministic functions (no LLM math)
    │
    ▼
Synthesis agent ──── interprets numbers into insight
    │
    ▼
Final answer
```

## The five tracks

| Track | Domain | Example question |
|---|---|---|
| Financial Performance | Margins, burn rate, ROI, revenue growth | "What's our gross margin trend this quarter?" |
| Operational Efficiency | Throughput, cycle time, utilization | "Where's the bottleneck in our pipeline?" |
| People Analytics | Headcount, attrition, productivity | "Are there distinct performance profiles on this team?" |
| Product Performance | Adoption, retention, funnels | "What does our activation funnel look like?" |
| Growth & Acquisition | CAC, LTV, churn | "Is our LTV:CAC ratio healthy?" |

The system is built to be modular — adding a 6th track means adding keywords to the router, writing the deterministic functions it needs, and wiring up one agent. No other part of the system changes.

## Design principles

- **Deterministic math, LLM interpretation.** Calculations never go through an LLM. This keeps numbers auditable and avoids hallucinated arithmetic.
- **Rules first, LLM as fallback.** Routing tries a cheap keyword match before spending tokens on a classification call. This keeps the system fast and cheap for the common case.
- **Optional enrichment, not default.** Features like clustering only run when the query actually asks for segmentation — running them unconditionally would produce noise on small or simple datasets.
- **Modularity over completeness.** The system ships with five tracks but is designed so new ones can be added without touching existing code paths.

## Project structure

```
src/
  agents.py      # ingestion agent, orchestrator, track agents, synthesis agent
  ai_model.py     # deterministic functions + Anthropic API wrapper + router config
app.py            # Streamlit frontend
main.py           # CLI entry point (useful for quick testing without the UI)
.env              # ANTHROPIC_API_KEY
```

## Running it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The CLI version (`main.py`) is also available for testing the pipeline directly without the UI — useful while developing a new track or debugging the router.

## Status

This is an early-stage MVP. Currently implemented: ingestion agent, orchestrator, and the Financial Performance track end-to-end. The remaining four tracks and the clustering enrichment layer are designed but not yet built — see the project's technical presentation for the full architecture and open questions.