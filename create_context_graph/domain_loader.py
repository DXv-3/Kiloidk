"""Domain loading utilities."""

from pathlib import Path

import yaml

from .domain import BaseOntology, DomainOntology, EntityType, merge_ontologies

DOMAINS_DIR = Path(__file__).parent / "domains"


def load_base_ontology() -> BaseOntology:
    """Load the base ontology."""
    return BaseOntology(
        entity_types=[
            EntityType(
                name="Document",
                description="A generic document entity",
                category="Objects",
                properties={
                    "content": {"type": "string"},
                    "created_at": {"type": "datetime"},
                    "updated_at": {"type": "datetime"},
                    "version": {"type": "integer", "default": 1},
                },
            ),
        ],
    )


def load_domain(name: str) -> DomainOntology | None:
    """Load a domain ontology by name."""
    domain_file = DOMAINS_DIR / f"{name}.yaml"
    if not domain_file.exists():
        return None

    with open(domain_file) as f:
        data = yaml.safe_load(f)

    domain = DomainOntology(**data)
    base = load_base_ontology()
    return merge_ontologies(base, domain)


def list_domains() -> list[str]:
    """List all available domains."""
    domains = []
    for f in DOMAINS_DIR.glob("*.yaml"):
        if f.stem != "_base":
            domains.append(f.stem)
    return sorted(domains)