# Multi-Agent Financial Analytics Copilot (`fin-copilot-mcp`)

[![CI/CD Pipeline](https://github.com/your-username/fin-copilot-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/fin-copilot-mcp/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade, deterministic multi-agent financial analytics engine built on Anthropic's **Model Context Protocol (MCP)** and **Claude 3.5 Sonnet**. The system processes complex natural language financial queries, translates them into dialect-validated PostgreSQL / DuckDB SQL, pulls live telemetry/market data, and executes a self-healing verification loop before presenting synthesized results.

---

## 🏗 Architecture & Agent Topology

The system uses specialized, domain-isolated agents decoupled from underlying tools using MCP JSON-RPC protocol standards.

```
                    ┌─────────────────────────────────────────┐
                    │       User Query Interface / API       │
                    └────────────────────┬────────────────────┘
                                         │
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │ Orchestrator Agent (Claude 3.5 Sonnet)  │
                    └────────────────────┬────────────────────┘
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         │ (MCP Protocol)                │ (MCP Protocol)                │ (MCP Protocol)
         ▼                               ▼                               ▼
┌──────────────────┐           ┌──────────────────┐           ┌──────────────────┐
│  mcp-server-sql  │           │mcp-server-stripe │           │mcp-server-market │
│ (PostgreSQL/Duck)│           │  (Billing Specs) │           │ (YFinance API)   │
└────────┬─────────┘           └──────────────────┘           └──────────────────┘
         │
         │ (Execution Error)
         ▼
┌──────────────────┐
│  Self-Healing    │ ── (Retry Stack Trace) ──► [ Orchestrator Agent ]
│  Validation Loop │
└──────────────────┘
```

---

## 🔑 Key Features

* **MCP-Native Architecture**: Fully decoupled tool servers using standard JSON-RPC over `stdio` / Server-Sent Events (SSE).
* **Self-Healing Text-to-SQL Loop**: Runs deterministic dry-run verification (`EXPLAIN`) before execution. Automatically captures AST/syntax errors and feeds stack traces back to Claude for up to 3 repair retries.
* **Double-Entry Validation**: Micro-agent verifying mathematical consistency, row cross-totals, and currency alignment prior to output synthesis.
* **Strict Type & Schema Safety**: Runtime validation via Pydantic v2 and static type checking with MyPy.
* **Cross-Platform Developer Experience**: Powers setup, linting, formatting, and testing on Windows (via PowerShell / `py`) and Linux/macOS seamlessly.

---

## 🛠 Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **LLM / Reasoning** | Claude 3.5 Sonnet (`anthropic`) | Intent decomposition, tool orchestration, and SQL generation |
| **Protocol Layer** | FastMCP / Model Context Protocol | Standardized tool/resource encapsulation over JSON-RPC |
| **Analytical Engine** | PostgreSQL / DuckDB / SQLite | OLAP/OLTP query execution, AST validation, and schema inspection |
| **Market Data** | Yahoo Finance (`yfinance`) | Macroeconomic benchmarks, equity quotes, and volume metrics |
| **Configuration** | `pydantic-settings` | Type-safe environment management and secret handling |
| **Developer Tooling** | `uv` / `pip`, `ruff`, `mypy`, `pytest` | Hermetic builds, linting, typing, and testing |

---

## 📁 Repository Structure

```text
fin-copilot-mcp/
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI pipeline (lint, type-check, unit & integration tests)
├── config/
│   └── mcp_servers.json          # System tool topologies and connection mappings
├── docker/
│   ├── Dockerfile.orchestrator    # Production container for agent runtime
│   └── Dockerfile.mcp-server      # Container specification for standalone MCP servers
├── src/
│   └── fin_copilot/
│       ├── core/                  # Base configuration, logging, exceptions
│       ├── mcp_servers/           # Standalone FastMCP server modules (SQL, Stripe, Market)
│       ├── agents/                # Orchestrator agent logic, prompts, and healing loops
│       └── utils/                 # Telemetry and formatting helpers
├── tests/
│   ├── unit/                      # FastMCP tool & resource unit tests
│   ├── integration/               # Multi-agent self-healing loop tests
│   └── evals/                     # Benchmarks for Text-to-SQL translation accuracy
├── scripts/
│   ├── setup.ps1                  # Windows PowerShell setup script
│   └── setup.sh                   # Linux / macOS bash setup script
├── pyproject.toml                 # Packaging, dependencies, and linter rules
├── .gitignore                     # Industry-standard Python ignore rules
├── .env.example                   # Environment variable template
└── README.md
```

---

## 🚀 Quickstart

### Prerequisites

* Python `>= 3.11`
* [uv](https://github.com/astral-sh/uv) or standard `pip`
* Anthropic API Key (`ANTHROPIC_API_KEY`)

### Installation & Setup

#### On Windows (PowerShell):
```powershell
# 1. Clone the repository
git clone https://github.com/your-username/fin-copilot-mcp.git
cd fin-copilot-mcp

# 2. Run PowerShell Setup Script
.\scripts\setup.ps1

# 3. Configure environment variables
Copy-Item .env.example .env
```

#### On Linux / macOS (Bash):
```bash
# 1. Clone the repository
git clone https://github.com/your-username/fin-copilot-mcp.git
cd fin-copilot-mcp

# 2. Run Setup Script
chmod +x ./scripts/setup.sh
./scripts/setup.sh

# 3. Configure environment variables
cp .env.example .env
```

---

## 🛡 Security & Guardrails

* **Read-Only Database Connections**: SQL MCP server limits execution strictly to SELECT statements and dialect dry-runs.
* **Token Sandboxing**: API keys are isolated within environment settings classes and never exposed across tool execution boundaries.
* **Data Masking**: Structural masking applied to sensitive financial attributes prior to model context generation.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.