# SDD Generator - Software Design Document Generation System

Version 0.1.0

## Overview

The SDD Generator is a comprehensive tool that implements the **Grok 4 Heavy** workflow for generating production-ready Software Design Documents (SDDs). It follows a two-phase approach:

1. **Phase 1: Requirements Interview** - Gathers project requirements through targeted questions
2. **Phase 2: SDD Draft Generation** - Generates a complete, structured SDD with all mandatory sections

## Features

- **Interactive Requirements Gathering**: Asks targeted multiple-choice questions about key architectural pillars
- **Compact Answer Format**: Supports efficient answer input (e.g., "1 C, 2 A, 3 B p95 500ms 99.9%, ...")
- **Comprehensive SDD Generation**: Produces ~1,800-2,500 word documents with:
  - Document Metadata
  - Executive Summary
  - Assumptions Register with confidence levels
  - Decision Log with rationale and alternatives
  - Trade-off Tables
  - Architecture Overview with Mermaid flowchart diagrams
  - Component descriptions
  - Data Model with Mermaid ER diagrams
  - API Design with OpenAPI 3.1 YAML
  - User Flows with Mermaid sequence diagrams
  - Non-Functional Requirements
  - Security and Privacy (STRIDE, OWASP ASVS, SOC 2 TSC, ISO/IEC 27001)
  - Observability, Testing, Deployment sections
  - Technology Choices with Provider Selection Matrix
  - Risks and Mitigations
  - Accessibility and Internationalization
  - Open Questions
  - Glossary

## Installation

No additional dependencies required beyond Python 3.7+.

```bash
cd sdd-generator
```

## Usage

### Command Line Interface

#### Show Interview Questions

```bash
python3 cli.py --name "MyApp" --description "A web application for managing tasks"
```

#### Generate SDD with Answers

```bash
python3 cli.py \
  --name "E-Commerce Platform" \
  --description "A modern e-commerce platform for selling products online" \
  --answers "1 A, 2 C, 3 C 10K-100K users p95 200ms 99.95%, 4 D GDPR SOC2, 5 A Stripe Okta, 6 B 6 months, 7 A, 8 F" \
  --output ecommerce-sdd.md
```

#### Interactive Mode

```bash
python3 cli.py \
  --name "MyApp" \
  --description "My application description" \
  --interactive
```

### Python API

```python
from workflow import SDDWorkflow

# Create workflow instance
workflow = SDDWorkflow()

# Option 1: Show questions first
workflow.run_phase1("MyApp", "A web application", None)

# Option 2: Generate SDD directly with answers
markdown = workflow.run_complete_workflow(
    project_name="E-Commerce Platform",
    description="A modern e-commerce platform",
    answer_string="1 A, 2 C, 3 B, 4 C Residency EU, 5 A Stripe, 6 D, 7 A, 8 F",
    output_file="sdd.md"
)

print(markdown)
```

## Interview Questions

The system asks 8 targeted questions covering key architectural pillars:

1. **Primary Users and Personas**: Who will use the application?
2. **Core Features and Scope**: What are the main features?
3. **Scale and SLOs**: What are latency/availability requirements?
4. **Data Sensitivity**: What is the data classification and compliance needs?
5. **External Integrations**: What third-party services are needed?
6. **Constraints**: Budget, timeline, team skills?
7. **Deployment Environment**: Which cloud provider?
8. **Baseline Archetype**: What architectural pattern?

## Answer Format

Answers are provided in a compact format:

```
"1 C, 2 A, 3 B p95 500ms 99.9%, 4 C Residency EU Class Confidential, 5 Other Stripe Okta, 6 B, 7 A, 8 F"
```

- Question number followed by selected option letter
- Additional context can be added after the option
- Use "skip" to skip a question and use defaults
- Separate answers with commas

## Output Format

The generated SDD is produced in clean Markdown format with:

- Proper heading hierarchy
- Tables for structured data
- Mermaid diagrams for visualizations
- YAML code blocks for API specifications
- Cross-references between sections
- Approximately 1,800-2,500 words

## Architecture

The system consists of five main modules:

- **`models.py`**: Data models for all SDD entities
- **`interviewer.py`**: Phase 1 requirements interview logic
- **`generator.py`**: Phase 2 SDD generation engine
- **`formatter.py`**: Markdown output formatting
- **`workflow.py`**: Orchestrates the complete workflow
- **`cli.py`**: Command-line interface

## Testing

Run the comprehensive test suite:

```bash
python3 test_sdd_generator.py
```

The test suite includes:
- Unit tests for all core functionality
- Integration tests for complete workflows
- Tests for all SDD sections
- Validation of output format and content

All 35 tests should pass with "OK".

## Security-First Approach

The generator defaults to best security practices:

- STRIDE threat modeling
- OWASP ASVS Level 2 compliance
- SOC 2 Trust Services Criteria alignment
- ISO/IEC 27001 control mappings
- Encryption at rest and in transit
- Principle of least privilege
- Comprehensive audit logging

Any deviations from security best practices are documented with rationale and residual risk assessment.

## Customization

The system is designed for easy customization:

- Add new questions by extending `RequirementsInterviewer._generate_questions()`
- Customize SDD sections by modifying methods in `SDDGenerator`
- Adjust output format by modifying `MarkdownFormatter`
- Add new data classifications or deployment environments in `models.py`

## Example Output

See the generated SDD examples in the `examples/` directory:

- `ecommerce-platform-sdd.md` - Full-featured e-commerce application
- `ml-prediction-service-sdd.md` - Machine learning service
- `mobile-backend-sdd.md` - Mobile application backend

## Assumptions and Defaults

When information is not provided, the system uses reasonable defaults:

- **Users**: General public users
- **Scale**: Up to 10,000 concurrent users
- **Availability**: 99.9% uptime SLA
- **Data Classification**: Internal
- **Architecture**: Cloud-native with managed services
- **Security**: Industry standard best practices

All assumptions are documented in the Assumptions Register with confidence levels.

## Compliance Frameworks

The generator includes mappings to major compliance frameworks:

- **STRIDE**: Threat modeling framework
- **OWASP ASVS**: Application Security Verification Standard
- **SOC 2**: Service Organization Control 2 Type II
- **ISO/IEC 27001**: Information security management
- **GDPR**: General Data Protection Regulation (when applicable)
- **HIPAA**: Health Insurance Portability and Accountability Act (when applicable)

## Contributing

This is an internal tool for generating software design documents. To contribute:

1. Ensure all tests pass
2. Follow existing code style
3. Add tests for new features
4. Update documentation

## License

Internal use only - Lifetime World / blogtheristo

## Version History

- **0.1.0** (2025-10-12): Initial implementation
  - Phase 1: Requirements Interview
  - Phase 2: SDD Generation
  - All mandatory sections
  - Comprehensive test coverage
  - CLI interface
