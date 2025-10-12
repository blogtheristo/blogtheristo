"""
Data models for SDD generation workflow
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum


class ConfidenceLevel(Enum):
    """Confidence levels for assumptions"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class DataClassification(Enum):
    """Data sensitivity classifications"""
    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    RESTRICTED = "Restricted"


class DeploymentEnvironment(Enum):
    """Supported deployment environments"""
    AWS = "AWS"
    AZURE = "Azure"
    GCP = "Google Cloud Platform"
    ON_PREMISE = "On-Premise"
    HYBRID = "Hybrid"


@dataclass
class Assumption:
    """Represents a single assumption in the SDD"""
    id: str
    description: str
    confidence: ConfidenceLevel
    source: str  # Where this assumption came from
    section: str  # Which section references this


@dataclass
class Decision:
    """Represents a decision in the decision log"""
    id: str
    description: str
    rationale: str
    alternatives: List[str]
    timestamp: str
    impact: str


@dataclass
class Question:
    """Represents a requirements interview question"""
    id: int
    text: str
    options: List[str]
    category: str  # e.g., "users", "features", "scale", etc.


@dataclass
class Answer:
    """Represents an answer to a requirements question"""
    question_id: int
    selected_option: str
    additional_context: Optional[str] = None


@dataclass
class ProjectRequirements:
    """Core project requirements gathered from Phase 1"""
    project_name: str
    description: str
    primary_users: List[str] = field(default_factory=list)
    core_features: List[str] = field(default_factory=list)
    scale_requirements: Dict[str, str] = field(default_factory=dict)
    data_classification: Optional[DataClassification] = None
    data_residency: Optional[str] = None
    compliance_requirements: List[str] = field(default_factory=list)
    external_integrations: List[str] = field(default_factory=list)
    constraints: Dict[str, str] = field(default_factory=dict)
    deployment_environment: Optional[DeploymentEnvironment] = None
    baseline_archetype: Optional[str] = None
    answers: List[Answer] = field(default_factory=list)


@dataclass
class SDDSection:
    """Represents a section in the SDD"""
    title: str
    content: str
    subsections: List['SDDSection'] = field(default_factory=list)


@dataclass
class SoftwareDesignDocument:
    """Complete Software Design Document structure"""
    metadata: Dict[str, str]
    executive_summary: str
    assumptions: List[Assumption] = field(default_factory=list)
    decisions: List[Decision] = field(default_factory=list)
    trade_offs: List[Dict[str, str]] = field(default_factory=list)
    architecture_overview: str = ""
    architecture_diagram: str = ""  # Mermaid diagram
    components: List[Dict[str, str]] = field(default_factory=list)
    data_model: str = ""  # Mermaid ER diagram
    api_design: str = ""  # OpenAPI 3.1 YAML
    user_flows: List[str] = field(default_factory=list)  # Mermaid sequence diagrams
    non_functional_requirements: Dict[str, str] = field(default_factory=dict)
    security_privacy: Dict[str, str] = field(default_factory=dict)
    observability: Dict[str, str] = field(default_factory=dict)
    testing_quality: Dict[str, str] = field(default_factory=dict)
    deployment_operations: Dict[str, str] = field(default_factory=dict)
    technology_choices: Dict[str, str] = field(default_factory=dict)
    risks_mitigations: List[Dict[str, str]] = field(default_factory=list)
    accessibility_i18n: Dict[str, str] = field(default_factory=dict)
    open_questions: List[str] = field(default_factory=list)
    glossary: Dict[str, str] = field(default_factory=dict)
