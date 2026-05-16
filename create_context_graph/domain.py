"""Domain ontology models."""

from typing import Any

from pydantic import BaseModel, Field, field_validator


class EntityType(BaseModel):
    """Entity type definition."""

    name: str
    description: str
    category: str  # POLE+O: People, Organizations, Locations, Events, Objects
    properties: dict[str, Any] = Field(default_factory=dict)

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        valid_categories = {"People", "Organizations", "Locations", "Events", "Objects"}
        if v not in valid_categories:
            raise ValueError(f"category must be one of {valid_categories}")
        return v


class Relationship(BaseModel):
    """Relationship type definition."""

    name: str
    source: str
    target: str
    description: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v[0].isupper():
            raise ValueError("Relationship name must start with uppercase letter")
        return v


class AgentTool(BaseModel):
    """Agent tool definition."""

    name: str
    description: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    cypher_template: str


class DocumentTemplate(BaseModel):
    """Document template for generation."""

    name: str
    document_type: str
    template: str
    variables: list[str] = Field(default_factory=list)


class DecisionTraceScenario(BaseModel):
    """Decision trace scenario for testing."""

    name: str
    description: str
    steps: list[str] = Field(default_factory=list)


class VisualizationConfig(BaseModel):
    """Graph visualization configuration."""

    node_colors: dict[str, str] = Field(default_factory=dict)
    edge_styles: dict[str, dict[str, Any]] = Field(default_factory=dict)
    layout: str = "force-directed"
    font: str = "default"


class DomainOntology(BaseModel):
    """Complete domain ontology definition."""

    name: str
    description: str
    version: str = "1.0.0"
    entity_types: list[EntityType] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)
    document_templates: list[DocumentTemplate] = Field(default_factory=list)
    decision_trace_scenarios: list[DecisionTraceScenario] = Field(default_factory=list)
    agent_tools: list[AgentTool] = Field(default_factory=list)
    system_prompt: str = ""
    visualization_config: VisualizationConfig = Field(default_factory=VisualizationConfig)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Domain name must be alphanumeric with hyphens/underscores")
        return v


class BaseOntology(BaseModel):
    """Base ontology inherited by all domains."""

    timestamp_property: str = "created_at"
    soft_delete_flag: str = "deleted_at"
    version_property: str = "version"
    document_entity: str = "Document"

    entity_types: list[EntityType] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)
    visualization_config: VisualizationConfig = Field(default_factory=VisualizationConfig)


def merge_ontologies(base: BaseOntology, domain: DomainOntology) -> DomainOntology:
    """Merge base ontology with domain ontology."""
    # Merge entity types - domain overrides base for same names
    base_entities = {e.name: e for e in base.entity_types}
    domain_entities = {e.name: e for e in domain.entity_types}

    # Domain entities override base entities
    merged_entities = list(base_entities.values())
    for name, entity in domain_entities.items():
        if name in base_entities:
            merged_entities.remove(base_entities[name])
        merged_entities.append(entity)

    # Merge relationships - concatenate lists
    merged_relationships = base.relationships + domain.relationships

    return DomainOntology(
        name=domain.name,
        description=domain.description,
        version=domain.version,
        entity_types=merged_entities,
        relationships=merged_relationships,
        document_templates=domain.document_templates,
        decision_trace_scenarios=domain.decision_trace_scenarios,
        agent_tools=domain.agent_tools,
        system_prompt=domain.system_prompt,
        visualization_config=domain.visualization_config,
    )