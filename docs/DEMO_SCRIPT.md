# ContextForge AI - 3 Minute Hackathon Demo Script

## 0:00 - 0:30 | The Problem
- **Speaker**: "Traditional AI code generators like ChatGPT generate generic code. They don't know your database schemas, downstream API impacts, data lineage, or team ownership. This leads to broken production code and hallucinated endpoints."

## 0:30 - 1:15 | The Solution & DataHub Integration
- **Speaker**: "Introducing ContextForge AI — the Metadata-Aware AI Engineering Platform powered by DataHub. Before writing a single line of code, our platform queries DataHub via MCP Server to inspect schema relationships, upstream/downstream lineage, and data governance rules."

## 1:15 - 2:15 | Live Demo (Workspace & Agent Execution)
- **Speaker**: "Watch us enter a prompt: 'Add EMI payment integration for orders table'. Instantly, the Multi-Agent system springs into action."
- **Visual**: Show Agent Timeline (Planner -> Context Agent -> Impact Analysis Agent -> Generator Agent).
- **Speaker**: "Notice how the Impact Analysis Agent flags a warning: 'Modifying total_amount will affect the downstream Analytics Pipeline'. The AI then generates safe, production-grade FastAPI endpoints and SQLAlchemy models with zero placeholder code."

## 2:15 - 3:00 | Conclusion & Devpost Pitch
- **Speaker**: "ContextForge AI brings true enterprise context to AI software engineering. Built with FastAPI, Next.js, LangGraph, and DataHub MCP. Thank you!"
