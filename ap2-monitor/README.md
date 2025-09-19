# AP2 Repository Monitoring Agent 0.1

The AP2 Repository Monitoring Agent is a Python tool designed to monitor GitHub repositories and generate comprehensive JSON reports with enhanced analysis capabilities.

## Features

- **Repository Rating System**: Tracks and sorts repositories by rating
- **Automated Explanations**: Generates intelligent analysis of repository usage patterns
- **DWS IQ Suitability Assessment**: Evaluates repositories for Digital Workspace Intelligence compatibility
- **Extensible Architecture**: Easy to customize criteria and add new analysis features

## Enhanced JSON Output

Each repository in the `top_rated` list now includes:

```json
{
  "name": "repository-name",
  "rating": 5,
  "url": "https://github.com/owner/repository-name",
  "explanation": "Python - versatile for data science, web development, and automation. highly popular with strong community adoption",
  "dws_iq_suitable": true
}
```

### New Fields

1. **`explanation`**: Automated analysis based on:
   - Programming language capabilities
   - Repository popularity (stars/forks)
   - Topic categorization (AI/ML, cloud-native, web development)
   - Community engagement metrics

2. **`dws_iq_suitable`**: Boolean assessment using customizable criteria:
   - Language suitability for DWS environments
   - Relevant topic tags
   - Quality thresholds (stars, rating)
   - Description keyword matching

## Usage

### Basic Usage

```python
from monitor import AP2Monitor, RepositoryData

# Create monitor instance
monitor = AP2Monitor()

# Add repositories
repo = RepositoryData(
    name="my-project",
    rating=4,
    url="https://github.com/user/my-project",
    description="A cloud-native application",
    topics=['python', 'cloud', 'kubernetes'],
    language="Python",
    stars=500,
    forks=100
)

monitor.add_repository(repo)

# Generate JSON report
json_report = monitor.generate_json_report()
print(json_report)
```

### Running the Example

```bash
cd ap2-monitor
python3 monitor.py
```

### Running Tests

```bash
cd ap2-monitor
python3 test_monitor.py
```

## Customizing DWS IQ Criteria

The DWS IQ suitability assessment can be easily customized by modifying the `_assess_dws_iq_suitability` method in `monitor.py`. Current criteria include:

- **Language Suitability**: Python, Go, JavaScript, TypeScript, C#, Java
- **Topic Relevance**: AI, cloud, microservices, automation, analytics
- **Quality Threshold**: Minimum 10 stars and rating ≥ 3
- **Description Keywords**: intelligent, digital, workspace, industry, etc.

### Example Customization

```python
def _assess_dws_iq_suitability(self, repo: RepositoryData) -> bool:
    # Add your custom criteria here
    suitable_criteria = []
    
    # Custom criterion 1: Specific language requirements
    if repo.language in ['Python', 'Go']:
        suitable_criteria.append(True)
    
    # Custom criterion 2: Business domain relevance
    business_topics = ['enterprise', 'saas', 'platform']
    if any(topic in repo.topics for topic in business_topics):
        suitable_criteria.append(True)
    
    # Repository is suitable if it meets your criteria
    return len(suitable_criteria) >= 1
```

## Architecture

- **`monitor.py`**: Main monitoring agent with analysis logic
- **`test_monitor.py`**: Comprehensive test suite
- **`RepositoryData`**: Data class for repository information
- **`AP2Monitor`**: Main monitoring class with extensible methods

## Dependencies

- Python 3.6+
- Standard library only (no external dependencies)

## Testing

The test suite includes:
- Unit tests for all core functionality
- Integration tests for complete workflows
- Test cases for both new fields
- Validation of JSON structure and content

Run tests with:
```bash
python3 test_monitor.py
```

All tests should pass with the message "OK".
