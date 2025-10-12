# Copilot Instructions for blogtheristo Repository

## Project Overview

This repository is part of the **Lifetime World** initiative, focused on fighting climate change, erosion, and droughts through AI innovation and sustainability solutions. The primary goal is to build and publish solutions that mitigate the effects of climate change using Agentic AI, Foundation Models, and Cloud technologies.

### Key Projects

- **AP2 Repository Monitoring Agent**: A Python-based monitoring system for GitHub repositories with intelligent analysis and DWS IQ (Digital Workspace Intelligence) suitability assessment.

## Technology Stack

### Primary Languages
- **Python 3.7+**: Primary language for AP2 Monitor and data processing
- **TypeScript/JavaScript**: For cloud-oriented programming
- **Go**: For high-performance concurrent systems
- **C#**: For Windows apps and enterprise systems (.NET MAUI, Blazor, Oqtane)

### Frameworks & Libraries
- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file generation
- **unittest**: Testing framework

### Cloud Platforms
- **AWS**: IAM, Amplify Studio, Aurora Serverless, Cognito, Comprehend, DynamoDB, DocumentDB, ECS, Redshift, SageMaker, CloudFormation, CodeCommit, CodePipeline, CodeStar, CodeDeploy, CodeBuild, CloudTrail, Organizations, Control Tower, QuickSight
- **Microsoft Azure**: Azure Marketplace solutions, AI Studio

### DevOps & Infrastructure
- **Containers**: Docker, Docker Swarm, Kubernetes, Helm, Terraform, AWS ECS, AWS Beanstalk, AWS EKS Anywhere
- **Monitoring**: Elasticsearch, Logstash, Kibana, Grafana, Prometheus, AWS CloudWatch
- **CI/CD**: GitHub Actions, YAML, JSON, Vault, Consul, Vagrant

## Coding Standards

### Python Code Style
- Use type hints for function parameters and return values
- Follow dataclass pattern for data structures (see `RepositoryData` in `ap2-monitor/monitor.py`)
- Use descriptive variable names that reflect the domain (e.g., `dws_iq_suitable`, `explanation`)
- Write docstrings for public methods
- Keep methods focused and single-purpose

### Testing
- Use `unittest` framework
- Write comprehensive test cases covering core functionality
- Include tests for edge cases and error conditions
- Test file naming convention: `test_<module>.py`
- Run tests with: `python3 test_monitor.py`

### File Organization
- Keep related functionality in modules (e.g., `ap2-monitor/` directory)
- Use `__init__.py` for package initialization and exports
- Include `requirements.txt` for Python dependencies
- Maintain separate `README.md` files for subdirectories with complex functionality

## Domain-Specific Context

### DWS IQ (Digital Workspace Intelligence)
When working with DWS IQ suitability assessments:
- Consider language suitability (Python, Go, TypeScript, C# are preferred)
- Evaluate relevant topic tags (cloud, kubernetes, ai, machine-learning, etc.)
- Apply quality thresholds (stars, ratings, community engagement)
- Match description keywords with domain relevance

### Repository Monitoring
The AP2 Monitor system:
- Rates and sorts repositories by rating
- Generates automated explanations based on language, topics, and popularity
- Assesses DWS IQ suitability using customizable criteria
- Produces JSON and Excel reports in `Results/` directory
- Uses date-based file naming: `Result<ddmmyyyy>.<ext>`

## Best Practices

### When Adding Features
1. Extend existing patterns (e.g., add new criteria to `_assess_dws_iq_suitability`)
2. Update tests to cover new functionality
3. Document changes in relevant README files
4. Ensure backward compatibility with existing reports

### When Modifying Code
1. Run tests before and after changes: `python3 test_monitor.py`
2. Keep changes minimal and focused
3. Preserve existing functionality unless explicitly changing behavior
4. Update docstrings if method signatures or behavior change

### File Naming Conventions
- Python modules: lowercase with underscores (e.g., `monitor.py`, `test_monitor.py`)
- Reports: `Result<ddmmyyyy>.<json|xlsx>` format
- Documentation: `README.md` in relevant directories

## Climate Tech & Sustainability Focus

When suggesting solutions or making decisions, prioritize:
- Energy efficiency and renewable energy integration
- Climate modeling and weather prediction capabilities
- Foundation models for scientific discovery (Aurora, DeepSpeed4Science, ClimaX)
- Cloud-native architectures for scalability
- AI agents for environmental stewardship

## Common Tasks

### Adding a New Repository to Monitor
```python
repo = RepositoryData(
    name="project-name",
    rating=4,
    url="https://github.com/user/project",
    description="Project description",
    topics=['topic1', 'topic2'],
    language="Python",
    stars=500,
    forks=100
)
monitor.add_repository(repo)
```

### Running the AP2 Monitor
```bash
cd ap2-monitor
python3 monitor.py
```

### Testing
```bash
cd ap2-monitor
python3 test_monitor.py
```

## Resources
- Main profile: blogtheristo 6.0
- Community: [onelifetime.world](https://onelifetime.world)
- Lifetime Fleet: [lifetime.fi/fleet](https://lifetime.fi/fleet)
- CV: [github.com/blogtheristo/cv](https://github.com/blogtheristo/cv)
