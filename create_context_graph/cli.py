"""CLI interface for create-context-graph."""

import sys
from pathlib import Path

import click
import questionary
from rich.console import Console
from rich.panel import Panel

from .config import (
    AgentFramework,
    DataSource,
    Neo4jConnectionType,
    ProjectConfig,
    SaaSConnector,
)
from .domain_loader import load_domain
from .scaffold import scaffold_project

console = Console()


# Valid options for validation
VALID_DOMAINS = [
    "healthcare", "software-engineering", "finance", "education", "legal",
    "marketing", "sales", "customer-support", "hr", "research", "manufacturing",
    "logistics", "hospitality", "media", "gaming", "real-estate", "insurance",
    "government", "nonprofit", "e-commerce", "iot", "generic", "custom",
]

VALID_FRAMEWORKS = [f.value for f in AgentFramework]
VALID_CONNECTORS = [c.value for c in SaaSConnector]


def pre_flight_validate(domain: str, framework: str, connectors: list[str]) -> bool:
    """Validate inputs before any filesystem operations."""
    valid = True

    if domain != "custom" and domain not in VALID_DOMAINS:
        console.print(f"[red]Error: Invalid domain '{domain}'. Valid domains: {', '.join(VALID_DOMAINS)}[/red]")
        valid = False

    if framework not in VALID_FRAMEWORKS:
        console.print(f"[red]Error: Invalid framework '{framework}'. Valid frameworks: {', '.join(VALID_FRAMEWORKS)}[/red]")
        valid = False

    for connector in connectors:
        if connector not in VALID_CONNECTORS:
            console.print(f"[red]Error: Invalid connector '{connector}'. Valid connectors: {', '.join(VALID_CONNECTORS)}[/red]")
            valid = False

    return valid


@click.command()
@click.option("--project-name", "-n", default="my-app", help="Project name")
@click.option("--data-source", type=click.Choice(["demo", "saas", "none"]), default="demo", help="Data source")
@click.option("--domain", "-d", default="healthcare", help="Domain / industry")
@click.option("--framework", "-f", default="pydanticai", help="Agent framework")
@click.option("--saas-connectors", multiple=True, help="SaaS connectors to include")
@click.option("--neo4j-connection", type=click.Choice(["local", "aura", "stub"]), default="stub", help="Neo4j connection type")
@click.option("--neo4j-uri", help="Neo4j URI")
@click.option("--neo4j-user", help="Neo4j username")
@click.option("--neo4j-password", help="Neo4j password")
@click.option("--anthropic-api-key", help="Anthropic API key")
@click.option("--openai-api-key", help="OpenAI API key")
@click.option("--google-api-key", help="Google API key")
@click.option("--custom-domain-description", help="Natural language description for custom domain")
@click.option("--skip-api-keys", is_flag=True, help="Skip API key prompts in interactive mode")
@click.option("--dry-run", is_flag=True, help="Show what would be generated without writing files")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--debug", is_flag=True, help="Debug output")
@click.option("--output-dir", "-o", help="Output directory")
@click.option("--skip-data-generation", is_flag=True, help="Skip synthetic data generation")
@click.option("--skip-saas-fetch", is_flag=True, help="Skip SaaS connector data fetching")
@click.option("--with-mcp", is_flag=True, help="Generate MCP server")
@click.option("--mcp-output-dir", help="MCP server output directory")
@click.option("--memory-strategy", default="per_conversation", help="Memory strategy")
@click.option("--memory-session-ttl", default=3600, help="Memory session TTL in seconds")
@click.option("--force", "-F", is_flag=True, help="Overwrite existing directory")
@click.version_option(package_name="create-context-graph")
def main(
    project_name: str,
    data_source: str,
    domain: str,
    framework: str,
    saas_connectors: tuple[str, ...],
    neo4j_connection: str,
    neo4j_uri: str | None,
    neo4j_user: str | None,
    neo4j_password: str | None,
    anthropic_api_key: str | None,
    openai_api_key: str | None,
    google_api_key: str | None,
    custom_domain_description: str | None,
    skip_api_keys: bool,
    dry_run: bool,
    verbose: bool,
    debug: bool,
    output_dir: str | None,
    skip_data_generation: bool,
    skip_saas_fetch: bool,
    with_mcp: bool,
    mcp_output_dir: str | None,
    memory_strategy: str,
    memory_session_ttl: int,
    force: bool,
) -> None:
    """Create a full-stack AI agent application backed by Neo4j knowledge graphs."""
    # Map MAF alias to anthropic-tools
    if framework == "maf":
        framework = "anthropic-tools"

    # Pre-flight validation
    if not pre_flight_validate(domain, framework, list(saas_connectors)):
        sys.exit(1)

    # Check for custom domain description when domain is custom
    if domain == "custom" and not custom_domain_description:
        console.print("[red]Error: --custom-domain-description is required when domain is 'custom'[/red]")
        sys.exit(1)

    # Check output directory
    output_path = Path(output_dir) if output_dir else Path.cwd() / project_name
    if output_path.exists() and any(output_path.iterdir()) and not force:
        console.print(Panel.fit(
            f"[red]Error:[/red] Directory '{output_path}' is not empty. Use --force to overwrite.",
            title="Directory Exists"
        ))
        sys.exit(1)

    config = ProjectConfig(
        project_name=project_name,
        data_source=DataSource(data_source),
        domain=domain,
        framework=AgentFramework(framework),
        saas_connectors=[SaaSConnector(c) for c in saas_connectors],
        neo4j_connection=Neo4jConnectionType(neo4j_connection),
        neo4j_uri=neo4j_uri,
        neo4j_user=neo4j_user,
        neo4j_password=neo4j_password,
        anthropic_api_key=anthropic_api_key,
        openai_api_key=openai_api_key,
        google_api_key=google_api_key,
        custom_domain_description=custom_domain_description,
        dry_run=dry_run,
        verbose=verbose,
        debug=debug,
        output_dir=str(output_path),
        skip_data_generation=skip_data_generation,
        skip_saas_fetch=skip_saas_fetch,
        with_mcp=with_mcp,
        mcp_output_dir=mcp_output_dir,
        force=force,
    )

    # Run scaffolding
    scaffold_project(config)


def run_interactive() -> None:
    """Run interactive wizard mode."""
    console.print(Panel.fit(
        "[bold blue]create-context-graph[/bold blue] - Full-stack AI agent scaffolding tool",
        subtitle="Interactive Wizard"
    ))

    project_name = questionary.text(
        "Project name:",
        default="my-app"
    ).unsafe_ask()

    data_source = questionary.select(
        "Data source:",
        choices=[
            questionary.Choice("Demo (synthetic data)", value="demo"),
            questionary.Choice("SaaS connectors", value="saas"),
            questionary.Choice("None", value="none"),
        ]
    ).unsafe_ask()

    domain = questionary.select(
        "Domain:",
        choices=[
            questionary.Choice("Healthcare", value="healthcare"),
            questionary.Choice("Software Engineering", value="software-engineering"),
            questionary.Choice("Finance", value="finance"),
            questionary.Choice("Education", value="education"),
            questionary.Choice("Legal", value="legal"),
            questionary.Choice("Custom...", value="custom"),
        ]
    ).unsafe_ask()

    custom_domain_description = None
    if domain == "custom":
        custom_domain_description = questionary.text(
            "Describe your domain (entities, relationships, use cases):"
        ).unsafe_ask()

    framework = questionary.select(
        "Agent framework:",
        choices=[
            questionary.Choice("PydanticAI", value="pydanticai"),
            questionary.Choice("Claude Agent SDK", value="claude-agent-sdk"),
            questionary.Choice("Strands", value="strands"),
            questionary.Choice("Google ADK", value="google-adk"),
            questionary.Choice("OpenAI Agents", value="openai-agents"),
            questionary.Choice("LangGraph", value="langgraph"),
            questionary.Choice("CrewAI", value="crewai"),
            questionary.Choice("Anthropic Tools", value="anthropic-tools"),
        ]
    ).unsafe_ask()

    neo4j_connection = questionary.select(
        "Neo4j connection:",
        choices=[
            questionary.Choice("Local (bolt://localhost:7688)", value="local"),
            questionary.Choice("Aura (cloud)", value="aura"),
            questionary.Choice("Stub (mock data)", value="stub"),
        ]
    ).unsafe_ask()

    # API keys (optional)
    console.print("\n[dim]API Keys (press Enter to skip):[/dim]")
    anthropic_key = questionary.password("Anthropic API key:").unsafe_ask() or None
    openai_key = questionary.password("OpenAI API key:").unsafe_ask() or None

    config = ProjectConfig(
        project_name=project_name,
        data_source=DataSource(data_source),
        domain=domain,
        framework=AgentFramework(framework),
        neo4j_connection=Neo4jConnectionType(neo4j_connection),
        custom_domain_description=custom_domain_description,
        anthropic_api_key=anthropic_key,
        openai_api_key=openai_key,
    )

    scaffold_project(config)


if __name__ == "__main__":
    # Check if running interactively (no args) or with CLI args
    if len(sys.argv) > 1:
        main()
    else:
        run_interactive()