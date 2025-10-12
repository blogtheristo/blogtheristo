"""
Phase 2: SDD Draft Generation Module
Generates complete Software Design Documents
"""

from datetime import datetime
from typing import List, Dict, Optional
try:
    from .models import (
        SoftwareDesignDocument, Assumption, Decision, ProjectRequirements,
        ConfidenceLevel, DataClassification
    )
except ImportError:
    from models import (
        SoftwareDesignDocument, Assumption, Decision, ProjectRequirements,
        ConfidenceLevel, DataClassification
    )


class SDDGenerator:
    """Generates Software Design Documents from requirements"""
    
    def __init__(self, requirements: ProjectRequirements):
        self.requirements = requirements
        self.assumptions: List[Assumption] = []
        self.decisions: List[Decision] = []
        self.assumption_counter = 1
        self.decision_counter = 1
    
    def add_assumption(
        self,
        description: str,
        confidence: ConfidenceLevel,
        source: str,
        section: str
    ) -> str:
        """Add an assumption and return its ID"""
        assumption_id = f"ASM-{self.assumption_counter:03d}"
        self.assumptions.append(Assumption(
            id=assumption_id,
            description=description,
            confidence=confidence,
            source=source,
            section=section
        ))
        self.assumption_counter += 1
        return assumption_id
    
    def add_decision(
        self,
        description: str,
        rationale: str,
        alternatives: List[str],
        impact: str
    ) -> str:
        """Add a decision and return its ID"""
        decision_id = f"DEC-{self.decision_counter:03d}"
        self.decisions.append(Decision(
            id=decision_id,
            description=description,
            rationale=rationale,
            alternatives=alternatives,
            timestamp=datetime.now().isoformat(),
            impact=impact
        ))
        self.decision_counter += 1
        return decision_id
    
    def generate(self) -> SoftwareDesignDocument:
        """Generate complete SDD"""
        sdd = SoftwareDesignDocument(
            metadata=self._generate_metadata(),
            executive_summary=self._generate_executive_summary(),
        )
        
        # Generate all sections
        self._populate_assumptions()
        self._populate_decisions()
        
        sdd.assumptions = self.assumptions
        sdd.decisions = self.decisions
        sdd.trade_offs = self._generate_trade_offs()
        sdd.architecture_overview = self._generate_architecture_overview()
        sdd.architecture_diagram = self._generate_architecture_diagram()
        sdd.components = self._generate_components()
        sdd.data_model = self._generate_data_model()
        sdd.api_design = self._generate_api_design()
        sdd.user_flows = self._generate_user_flows()
        sdd.non_functional_requirements = self._generate_nfrs()
        sdd.security_privacy = self._generate_security_privacy()
        sdd.observability = self._generate_observability()
        sdd.testing_quality = self._generate_testing_quality()
        sdd.deployment_operations = self._generate_deployment_operations()
        sdd.technology_choices = self._generate_technology_choices()
        sdd.risks_mitigations = self._generate_risks_mitigations()
        sdd.accessibility_i18n = self._generate_accessibility_i18n()
        sdd.open_questions = self._generate_open_questions()
        sdd.glossary = self._generate_glossary()
        
        return sdd
    
    def _generate_metadata(self) -> Dict[str, str]:
        """Generate document metadata"""
        return {
            "title": f"Software Design Document - {self.requirements.project_name}",
            "version": "1.0",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "author": "SDD Generator - Grok 4 Heavy",
            "status": "Draft"
        }
    
    def _generate_executive_summary(self) -> str:
        """Generate executive summary"""
        env = self.requirements.deployment_environment.value if self.requirements.deployment_environment else "cloud"
        archetype = self.requirements.baseline_archetype or "web application"
        
        summary = f"""
## Executive Summary

This document describes the software design for {self.requirements.project_name}.

**Project Overview:** {self.requirements.description}

**Target Users:** {', '.join(self.requirements.primary_users) if self.requirements.primary_users else 'To be determined'}

**Architecture:** {archetype} deployed on {env}

**Key Objectives:**
- Deliver a scalable, secure, and maintainable solution
- Meet specified performance and availability requirements
- Ensure compliance with security and privacy standards
- Provide excellent user experience

This design prioritizes security, scalability, and operational excellence while balancing cost and development velocity.
"""
        return summary.strip()
    
    def _populate_assumptions(self):
        """Generate assumptions register"""
        # Add default assumptions based on requirements
        if not self.requirements.primary_users:
            self.add_assumption(
                "User base consists of general public users",
                ConfidenceLevel.MEDIUM,
                "Default assumption",
                "User Requirements"
            )
        
        if not self.requirements.scale_requirements:
            self.add_assumption(
                "System should support up to 10,000 concurrent users",
                ConfidenceLevel.LOW,
                "Default assumption",
                "Non-Functional Requirements"
            )
        
        if self.requirements.deployment_environment:
            self.add_assumption(
                f"Deployment will use managed services from {self.requirements.deployment_environment.value}",
                ConfidenceLevel.HIGH,
                "User specified",
                "Deployment"
            )
    
    def _populate_decisions(self):
        """Generate decision log"""
        # Add key architectural decisions
        if self.requirements.deployment_environment:
            env = self.requirements.deployment_environment.value
            self.add_decision(
                f"Use {env} as primary cloud provider",
                f"Selected based on user requirements and organizational alignment",
                ["AWS", "Azure", "GCP", "On-Premise"],
                "High - affects all infrastructure decisions"
            )
        
        if self.requirements.baseline_archetype:
            self.add_decision(
                f"Adopt {self.requirements.baseline_archetype} architecture pattern",
                "Aligns with project requirements and team expertise",
                ["Monolithic", "Microservices", "Serverless", "Event-driven"],
                "High - defines overall system structure"
            )
    
    def _generate_trade_offs(self) -> List[Dict[str, str]]:
        """Generate trade-off table"""
        return [
            {
                "aspect": "Architecture Complexity",
                "option_a": "Microservices",
                "option_b": "Monolithic",
                "chosen": "Microservices" if self.requirements.baseline_archetype == "Microservices" else "Monolithic",
                "rationale": "Better scalability and team autonomy vs simpler operations"
            },
            {
                "aspect": "Database",
                "option_a": "SQL (PostgreSQL)",
                "option_b": "NoSQL (DynamoDB)",
                "chosen": "SQL (PostgreSQL)",
                "rationale": "ACID compliance and complex queries vs horizontal scalability"
            },
            {
                "aspect": "Deployment",
                "option_a": "Kubernetes",
                "option_b": "Managed Services",
                "chosen": "Managed Services",
                "rationale": "Less operational overhead vs more control and portability"
            }
        ]
    
    def _generate_architecture_overview(self) -> str:
        """Generate architecture overview text"""
        overview = f"""
## Architecture Overview

The system follows a {self.requirements.baseline_archetype or 'cloud-native'} architecture pattern.

**Key Architectural Principles:**
- **Scalability:** Design for horizontal scaling
- **Security:** Security-first approach with defense in depth
- **Resilience:** Design for failure with graceful degradation
- **Observability:** Comprehensive monitoring and logging
- **Maintainability:** Clear separation of concerns and modular design

**High-Level Architecture:**
The system is decomposed into the following layers:
- **Presentation Layer:** User-facing interfaces (web, mobile, API)
- **Application Layer:** Business logic and orchestration
- **Data Layer:** Persistent storage and caching
- **Integration Layer:** External service integrations
"""
        return overview.strip()
    
    def _generate_architecture_diagram(self) -> str:
        """Generate Mermaid architecture flowchart"""
        return """
```mermaid
flowchart TD
    User[User] --> LB[Load Balancer]
    LB --> Web[Web Application]
    LB --> API[API Gateway]
    
    Web --> App[Application Server]
    API --> App
    
    App --> Auth[Authentication Service]
    App --> Bus[Business Logic]
    
    Bus --> Cache[Redis Cache]
    Bus --> DB[(Database)]
    Bus --> Queue[Message Queue]
    
    Queue --> Worker[Background Workers]
    Worker --> DB
    
    App --> Ext[External Services]
    
    Monitor[Monitoring] -.-> Web
    Monitor -.-> API
    Monitor -.-> App
    Monitor -.-> Worker
```
"""
    
    def _generate_components(self) -> List[Dict[str, str]]:
        """Generate component descriptions"""
        components = [
            {
                "name": "API Gateway",
                "responsibility": "Request routing, authentication, rate limiting",
                "technology": "AWS API Gateway / Azure API Management",
                "interfaces": "REST API, WebSocket"
            },
            {
                "name": "Application Server",
                "responsibility": "Business logic execution, orchestration",
                "technology": "Node.js / Python / Java",
                "interfaces": "Internal APIs"
            },
            {
                "name": "Database",
                "responsibility": "Persistent data storage",
                "technology": "PostgreSQL / DynamoDB",
                "interfaces": "Database protocol"
            },
            {
                "name": "Cache",
                "responsibility": "High-speed data caching",
                "technology": "Redis / Memcached",
                "interfaces": "Cache protocol"
            },
            {
                "name": "Message Queue",
                "responsibility": "Asynchronous task processing",
                "technology": "RabbitMQ / AWS SQS",
                "interfaces": "Queue protocol"
            }
        ]
        return components
    
    def _generate_data_model(self) -> str:
        """Generate Mermaid ER diagram"""
        return """
```mermaid
erDiagram
    USER ||--o{ SESSION : has
    USER ||--o{ ORDER : places
    USER {
        string id PK
        string email
        string name
        datetime created_at
        datetime updated_at
    }
    
    SESSION {
        string id PK
        string user_id FK
        datetime expires_at
        string token
    }
    
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        string id PK
        string user_id FK
        decimal total
        string status
        datetime created_at
    }
    
    ORDER_ITEM }o--|| PRODUCT : references
    ORDER_ITEM {
        string id PK
        string order_id FK
        string product_id FK
        int quantity
        decimal price
    }
    
    PRODUCT {
        string id PK
        string name
        string description
        decimal price
        int stock
    }
```
"""
    
    def _generate_api_design(self) -> str:
        """Generate OpenAPI 3.1 YAML fragment"""
        return """
```yaml
openapi: 3.1.0
info:
  title: """ + self.requirements.project_name + """ API
  version: 1.0.0
  description: API for """ + self.requirements.project_name + """

servers:
  - url: https://api.example.com/v1
    description: Production server

paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      tags:
        - users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
    
    post:
      summary: Create user
      operationId: createUser
      tags:
        - users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        created_at:
          type: string
          format: date-time
    
    UserCreate:
      type: object
      required:
        - email
        - name
      properties:
        email:
          type: string
          format: email
        name:
          type: string
  
  responses:
    UnauthorizedError:
      description: Authentication required
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```
"""
    
    def _generate_user_flows(self) -> List[str]:
        """Generate Mermaid sequence diagrams"""
        return [
            """
```mermaid
sequenceDiagram
    actor User
    participant Web as Web App
    participant API as API Gateway
    participant Auth as Auth Service
    participant DB as Database
    
    User->>Web: Access application
    Web->>API: Request authentication
    API->>Auth: Validate credentials
    Auth->>DB: Check user
    DB-->>Auth: User data
    Auth-->>API: JWT token
    API-->>Web: Authentication success
    Web-->>User: Display dashboard
```
""",
            """
```mermaid
sequenceDiagram
    actor User
    participant App as Application
    participant Bus as Business Logic
    participant DB as Database
    participant Queue as Message Queue
    participant Worker as Background Worker
    
    User->>App: Submit order
    App->>Bus: Process order
    Bus->>DB: Save order
    DB-->>Bus: Order saved
    Bus->>Queue: Queue notification
    Bus-->>App: Order accepted
    App-->>User: Confirmation
    Queue->>Worker: Process notification
    Worker->>User: Send email
```
"""
        ]
    
    def _generate_nfrs(self) -> Dict[str, str]:
        """Generate non-functional requirements"""
        scale = self.requirements.scale_requirements.get("details", "standard performance") if self.requirements.scale_requirements else "standard performance"
        
        return {
            "Performance": f"System must meet {scale}. Response times under 500ms for 95th percentile.",
            "Scalability": "Support horizontal scaling to handle 10x traffic growth",
            "Availability": "99.9% uptime SLA (8.76 hours downtime per year)",
            "Reliability": "Mean Time Between Failures (MTBF) > 720 hours",
            "Maintainability": "Code coverage > 80%, automated deployments",
            "Security": "SOC 2 Type II compliance, encryption at rest and in transit",
            "Usability": "WCAG 2.1 AA compliance, responsive design",
            "Portability": "Cloud-agnostic design where feasible"
        }
    
    def _generate_security_privacy(self) -> Dict[str, str]:
        """Generate security and privacy section with frameworks"""
        classification = self.requirements.data_classification.value if self.requirements.data_classification else "Internal"
        compliance = ', '.join(self.requirements.compliance_requirements) if self.requirements.compliance_requirements else "Industry standards"
        
        return {
            "overview": f"Data Classification: {classification}. Compliance: {compliance}",
            "stride_threats": """
**STRIDE Threat Model:**
- **Spoofing:** Mitigated by multi-factor authentication (MFA)
- **Tampering:** Mitigated by input validation and integrity checks
- **Repudiation:** Mitigated by comprehensive audit logging
- **Information Disclosure:** Mitigated by encryption and access controls
- **Denial of Service:** Mitigated by rate limiting and DDoS protection
- **Elevation of Privilege:** Mitigated by principle of least privilege
""",
            "owasp_asvs": """
**OWASP ASVS Compliance:**
- V1: Architecture, Design and Threat Modeling (Level 2)
- V2: Authentication (Level 2)
- V3: Session Management (Level 2)
- V4: Access Control (Level 2)
- V7: Error Handling and Logging (Level 2)
- V8: Data Protection (Level 2)
- V9: Communications (Level 2)
""",
            "soc2_tsc": """
**SOC 2 Trust Services Criteria:**
- CC1: Control Environment
- CC2: Communication and Information
- CC3: Risk Assessment
- CC4: Monitoring Activities
- CC5: Control Activities
- CC6: Logical and Physical Access Controls
- CC7: System Operations
""",
            "iso27001": """
**ISO/IEC 27001 Controls:**
- A.5: Information Security Policies
- A.6: Organization of Information Security
- A.8: Asset Management
- A.9: Access Control
- A.12: Operations Security
- A.13: Communications Security
- A.14: System Acquisition, Development and Maintenance
- A.18: Compliance
""",
            "ai_safety": """
**AI Safety (if applicable):**
- Model bias detection and mitigation
- Explainability and transparency
- Privacy-preserving techniques
- Continuous monitoring for drift
- Human-in-the-loop for critical decisions
"""
        }
    
    def _generate_observability(self) -> Dict[str, str]:
        """Generate observability section"""
        return {
            "Logging": "Structured logging with correlation IDs, centralized via ELK/CloudWatch",
            "Metrics": "Golden signals (latency, traffic, errors, saturation) via Prometheus/CloudWatch",
            "Tracing": "Distributed tracing with OpenTelemetry/X-Ray",
            "Alerting": "PagerDuty/Opsgenie integration for critical alerts",
            "Dashboards": "Grafana/CloudWatch dashboards for operations team",
            "SLIs/SLOs": "Defined SLIs tracked against SLOs with error budgets"
        }
    
    def _generate_testing_quality(self) -> Dict[str, str]:
        """Generate testing and quality section"""
        return {
            "Unit Testing": "JUnit/pytest with 80%+ code coverage",
            "Integration Testing": "API tests with test containers",
            "E2E Testing": "Selenium/Playwright for critical user journeys",
            "Performance Testing": "Load testing with k6/JMeter",
            "Security Testing": "SAST (SonarQube), DAST (OWASP ZAP), dependency scanning",
            "Quality Gates": "CI/CD pipeline blocks on test failures or coverage drops",
            "Code Review": "Mandatory peer review with automated linting"
        }
    
    def _generate_deployment_operations(self) -> Dict[str, str]:
        """Generate deployment and operations section"""
        env = self.requirements.deployment_environment.value if self.requirements.deployment_environment else "Cloud"
        
        return {
            "Environment": env,
            "CI/CD": "GitHub Actions/GitLab CI with automated testing and deployment",
            "Infrastructure as Code": "Terraform/CloudFormation for reproducible infrastructure",
            "Deployment Strategy": "Blue-green deployments with automated rollback",
            "Configuration Management": "Environment variables via secrets manager",
            "Disaster Recovery": "RTO: 4 hours, RPO: 1 hour, automated backups",
            "Runbooks": "Documented procedures for common incidents"
        }
    
    def _generate_technology_choices(self) -> Dict[str, str]:
        """Generate technology choices and trade-offs"""
        env = self.requirements.deployment_environment.value if self.requirements.deployment_environment else "AWS"
        
        choices = {
            "Programming Language": "Python/Node.js/Java (based on team expertise)",
            "Web Framework": "FastAPI/Express/Spring Boot",
            "Database": "PostgreSQL (RDS/CloudSQL) for relational data",
            "Cache": "Redis (ElastiCache/Cloud Memorystore)",
            "Message Queue": "RabbitMQ/AWS SQS/Azure Service Bus",
            "API Gateway": f"{env} API Gateway",
            "Authentication": "OAuth 2.0 + OIDC with Auth0/Cognito",
            "Monitoring": "DataDog/CloudWatch + Grafana",
            "CDN": "CloudFront/CloudFlare for static assets"
        }
        
        # Provider selection matrix
        choices["Provider_Matrix"] = f"""
**Provider Selection Matrix:**

| Criterion | AWS | Azure | GCP | Selected |
|-----------|-----|-------|-----|----------|
| Maturity | High | High | Medium | {env} |
| Cost | Medium | Medium | Low | {env} |
| Team Skills | High | Medium | Low | {env} |
| Compliance | High | High | Medium | {env} |
| Managed Services | High | High | High | {env} |
"""
        
        return choices
    
    def _generate_risks_mitigations(self) -> List[Dict[str, str]]:
        """Generate risks and mitigations"""
        return [
            {
                "risk": "Vendor Lock-in",
                "likelihood": "Medium",
                "impact": "High",
                "mitigation": "Use cloud-agnostic abstractions where possible, document migration paths"
            },
            {
                "risk": "Data Breach",
                "likelihood": "Low",
                "impact": "Critical",
                "mitigation": "Encryption, access controls, regular security audits, incident response plan"
            },
            {
                "risk": "Performance Degradation",
                "likelihood": "Medium",
                "impact": "Medium",
                "mitigation": "Load testing, auto-scaling, performance monitoring, caching strategy"
            },
            {
                "risk": "Third-party Service Outage",
                "likelihood": "Medium",
                "impact": "High",
                "mitigation": "Fallback mechanisms, circuit breakers, SLA monitoring"
            },
            {
                "risk": "Team Knowledge Gaps",
                "likelihood": "Medium",
                "impact": "Medium",
                "mitigation": "Training programs, documentation, pair programming, knowledge sharing"
            }
        ]
    
    def _generate_accessibility_i18n(self) -> Dict[str, str]:
        """Generate accessibility and internationalization section"""
        return {
            "Accessibility": "WCAG 2.1 Level AA compliance, keyboard navigation, screen reader support",
            "Internationalization": "i18n framework (i18next/gettext), RTL support",
            "Localization": "Support for multiple languages (English, Spanish, French initially)",
            "Time Zones": "UTC storage, user timezone conversion",
            "Currency": "Multi-currency support if applicable",
            "Date/Number Formats": "Locale-specific formatting"
        }
    
    def _generate_open_questions(self) -> List[str]:
        """Generate list of open questions"""
        questions = []
        
        if not self.requirements.primary_users:
            questions.append("Q1: Who are the primary users and what are their specific needs?")
        
        if not self.requirements.scale_requirements:
            questions.append("Q2: What are the expected scale and performance requirements?")
        
        if not self.requirements.external_integrations:
            questions.append("Q3: What external services need to be integrated?")
        
        if not self.requirements.constraints:
            questions.append("Q4: What are the budget and timeline constraints?")
        
        # Always add some technical open questions
        questions.extend([
            "Q: What is the disaster recovery strategy for different failure scenarios?",
            "Q: What are the specific data retention requirements?",
            "Q: How will we handle schema migrations in production?",
            "Q: What are the specific audit log retention policies?"
        ])
        
        return questions
    
    def _generate_glossary(self) -> Dict[str, str]:
        """Generate glossary of terms"""
        return {
            "API": "Application Programming Interface",
            "CDN": "Content Delivery Network",
            "GDPR": "General Data Protection Regulation",
            "JWT": "JSON Web Token",
            "MFA": "Multi-Factor Authentication",
            "MTBF": "Mean Time Between Failures",
            "NFR": "Non-Functional Requirement",
            "OIDC": "OpenID Connect",
            "RTO": "Recovery Time Objective",
            "RPO": "Recovery Point Objective",
            "SLA": "Service Level Agreement",
            "SLI": "Service Level Indicator",
            "SLO": "Service Level Objective",
            "SOC 2": "Service Organization Control 2",
            "STRIDE": "Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege",
            "WCAG": "Web Content Accessibility Guidelines"
        }
