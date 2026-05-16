"""Core configuration models for create-context-graph."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DataSource(str, Enum):
    DEMO = "demo"
    SAAS = "saas"
    NONE = "none"


class Neo4jConnectionType(str, Enum):
    LOCAL = "local"
    AURA = "aura"
    STUB = "stub"


class AgentFramework(str, Enum):
    PYDANTIC_AI = "pydanticai"
    CLAUDE_AGENT_SDK = "claude-agent-sdk"
    STRANDS = "strands"
    GOOGLE_ADK = "google-adk"
    OPENAI_AGENTS = "openai-agents"
    LANGGRAPH = "langgraph"
    CREWAI = "crewai"
    ANTHROPIC_TOOLS = "anthropic-tools"
    MAF = "maf"  # alias for anthropic-tools


class SaaSConnector(str, Enum):
    GITHUB = "github"
    SLACK = "slack"
    JIRA = "jira"
    NOTION = "notion"
    GMAIL = "gmail"
    GOOGLE_CALENDAR = "google-calendar"
    SALESFORCE = "salesforce"
    LINEAR = "linear"
    GOOGLE_WORKSPACE = "google-workspace"
    CLAUDE_CODE = "claude-code"
    CLAUDE_AI = "claude-ai"
    CHATGPT = "chatgpt"


class ProjectConfig(BaseModel):
    """Shared configuration model for both CLI and interactive modes."""

    project_name: str = Field(default="my-app")
    data_source: DataSource = DataSource.DEMO
    domain: str = "healthcare"
    framework: AgentFramework = AgentFramework.PYDANTIC_AI
    saas_connectors: list[SaaSConnector] = Field(default_factory=list)
    neo4j_connection: Neo4jConnectionType = Neo4jConnectionType.STUB
    neo4j_uri: str | None = None
    neo4j_user: str | None = None
    neo4j_password: str | None = None
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None
    google_api_key: str | None = None
    custom_domain_description: str | None = None
    dry_run: bool = False
    verbose: bool = False
    debug: bool = False
    output_dir: str | None = None
    skip_data_generation: bool = False
    skip_saas_fetch: bool = False
    with_mcp: bool = False
    mcp_output_dir: str | None = None
    memory_strategy: str = "per_conversation"
    memory_session_ttl: int = 3600
    force: bool = False

    def to_cli_args(self) -> list[str]:
        """Convert config to CLI argument list for reproducibility."""
        args = [
            "--project-name", self.project_name,
            "--data-source", self.data_source.value,
            "--domain", self.domain,
            "--framework", self.framework.value,
            "--neo4j-connection", self.neo4j_connection.value,
        ]

        if self.saas_connectors:
            args.extend(["--saas-connectors"] + [c.value for c in self.saas_connectors])

        if self.neo4j_uri:
            args.extend(["--neo4j-uri", self.neo4j_uri])
        if self.neo4j_user:
            args.extend(["--neo4j-user", self.neo4j_user])
        if self.neo4j_password:
            args.extend(["--neo4j-password", self.neo4j_password])

        if self.dry_run:
            args.append("--dry-run")
        if self.verbose:
            args.append("--verbose")
        if self.debug:
            args.append("--debug")
        if self.output_dir:
            args.extend(["--output-dir", self.output_dir])
        if self.skip_data_generation:
            args.append("--skip-data-generation")
        if self.skip_saas_fetch:
            args.append("--skip-saas-fetch")
        if self.with_mcp:
            args.append("--with-mcp")
        if self.mcp_output_dir:
            args.extend(["--mcp-output-dir", self.mcp_output_dir])
        if self.force:
            args.append("--force")

        return args