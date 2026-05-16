"""Project scaffolding logic."""

import json
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from .config import ProjectConfig
from .domain import DomainOntology
from .domain_loader import load_domain

console = Console()


def scaffold_project(config: ProjectConfig) -> None:
    """Execute the 8-stage scaffolding pipeline."""
    console.print(Panel("[bold]Stage 1:[/bold] Loading ontology..."))

    domain = load_domain(config.domain)
    if domain is None:
        console.print(f"[red]Error: Domain '{config.domain}' not found[/red]")
        raise SystemExit(1)

    console.print(Panel("[bold]Stage 2:[/bold] Custom domain generation..."))

    if config.domain == "custom" and config.custom_domain_description:
        console.print("[yellow]Custom domain generation not yet implemented[/yellow]")

    output_dir = Path(config.output_dir or config.project_name)

    _render_templates(config, domain, output_dir)

    console.print(Panel("[bold]Stage 4-8:[/bold] Data generation and ingestion..."))

    _generate_mock_data(config, output_dir, domain)

    _print_summary(config, output_dir, domain)


def _render_templates(
    config: ProjectConfig,
    domain: DomainOntology,
    output_dir: Path,
) -> None:
    """Render all project templates."""
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "backend").mkdir(exist_ok=True)

    main_py = '''"""FastAPI backend for AI agent application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

app = FastAPI(title="AI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    history: list = []


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "neo4j": "stubbed"}


@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint."""
    return {"text": f"Response to: {request.message}", "tool_calls": [], "entities_extracted": [], "preferences_detected": []}


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint."""
    async def generate():
        data = {"type": "text_delta", "content": "Hello"}
        yield f"data: {json.dumps(data)}\\n\\n"
        data = {"type": "done"}
        yield f"data: {json.dumps(data)}\\n\\n"
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/schema/visualization")
async def schema_visualization():
    """Graph schema for visualization."""
    return {
        "nodes": [{"id": "Patient", "label": "Patient", "color": "#4CAF50"}],
        "edges": []
    }
'''
    (output_dir / "backend" / "main.py").write_text(main_py)

    models_py = '''"""Pydantic models for the AI agent application."""
from typing import Any
from pydantic import BaseModel


class ToolCall(BaseModel):
    name: str
    input: dict[str, Any]
    output: dict[str, Any]
    duration: float = 0.0


class AgentResponse(BaseModel):
    text: str
    tool_calls: list[ToolCall] = []
    entities_extracted: list[dict] = []
    preferences_detected: list[dict] = []
'''
    (output_dir / "backend" / "models.py").write_text(models_py)

    (output_dir / "frontend").mkdir(exist_ok=True)

    package_json = {
        "name": config.project_name,
        "version": "0.1.0",
        "private": True,
        "scripts": {"dev": "next dev", "build": "next build", "start": "next start"},
        "dependencies": {"next": "^16.0.0", "react": "^19.0.0", "react-dom": "^19.0.0"},
    }
    (output_dir / "frontend" / "package.json").write_text(json.dumps(package_json, indent=2))

    makefile = '''.PHONY: install start start-backend start-frontend docker-up docker-down seed reset test lint format type-check build clean health

install:
\tbun install --cwd frontend
\tpip install -e .

start: start-backend start-frontend

start-backend:
\tuvicorn backend.main:app --reload --port 8000

start-frontend:
\tcd frontend && bun dev

docker-up:
\tdocker-compose up -d

docker-down:
\tdocker-compose down

seed:
\techo "Seeding data..."

reset:
\techo "Resetting..."

test:
\techo "Testing..."

lint:
\truff check backend
\tcd frontend && eslint .

format:
\truff format backend
\tcd frontend && prettier --write .

type-check:
\tmypy backend
\tcd frontend && tsc --noEmit

build:
\tcd frontend && bun build

clean:
\tfind . -type d -name "__pycache__" -exec rm -rf {} +
\trm -rf node_modules .next

health:
\tcurl http://localhost:8000/health
'''
    (output_dir / "Makefile").write_text(makefile)

    docker_compose = '''version: "3.8"
services:
  neo4j:
    image: neo4j:5-community
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - neo4j_data:/data
    environment:
      - NEO4J_AUTH=neo4j/password

volumes:
  neo4j_data:
'''
    (output_dir / "docker-compose.yml").write_text(docker_compose)

    readme = f'''# {config.project_name}

A full-stack AI agent application generated by create-context-graph.

## Quick Start

```bash
make install
make start
```

## API

- `GET /health` - Health check
- `POST /chat` - Chat endpoint
- `POST /chat/stream` - Streaming chat
'''
    (output_dir / "README.md").write_text(readme)

    (output_dir / "data" / "fixtures").mkdir(parents=True, exist_ok=True)
    (output_dir / "data" / "fixtures" / "entities.json").write_text("[]")


def _generate_mock_data(config: ProjectConfig, output_dir: Path, domain: DomainOntology) -> None:
    """Generate mock data for the domain."""
    entities = []

    for entity_type in domain.entity_types[:5]:
        for i in range(10):
            entities.append({
                "id": f"{entity_type.name.lower()}_{i}",
                "type": entity_type.name,
                "name": f"Sample {entity_type.name} {i}",
                "description": f"Description for {entity_type.name} {i}",
            })

    (output_dir / "data" / "fixtures" / "entities.json").write_text(json.dumps(entities, indent=2))


def _print_summary(config: ProjectConfig, output_dir: Path, domain: DomainOntology) -> None:
    """Print project summary."""
    from rich.table import Table

    table = Table(title="Project Summary")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Project Name", config.project_name)
    table.add_row("Domain", config.domain)
    table.add_row("Framework", config.framework.value)
    table.add_row("Data Source", config.data_source.value)
    table.add_row("Neo4j", config.neo4j_connection.value)
    table.add_row("Output", str(output_dir))

    console.print(table)
    console.print("\n[bold green]Project generated successfully![/bold green]")
    console.print(f"\nNext steps:\n  cd {config.project_name}\n  make install\n  make start")