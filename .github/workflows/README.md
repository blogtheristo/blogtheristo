# AP2 Monitor GitHub Actions Workflow

This document describes the comprehensive CI/CD workflow created for the AP2 Repository Monitoring Agent.

## Workflow Overview

The workflow (`ap2-monitor.yml`) provides automated testing, code quality checks, and integration validation for the ap2-monitor project.

## Triggers

The workflow runs on:
- **Push**: To `main` or `develop` branches (when ap2-monitor files change)
- **Pull Request**: Against `main` or `develop` branches (when ap2-monitor files change)
- **Schedule**: Daily at 6 AM UTC
- **Manual**: Via GitHub UI workflow dispatch

## Jobs

### 1. Test Job (`test`)
- **Platforms**: Ubuntu, Windows, macOS
- **Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Features**:
  - Dependency installation with pip caching
  - Flake8 linting for syntax errors
  - Test execution with coverage reporting
  - Report generation validation
  - Artifact upload (test reports)

### 2. Code Quality Job (`code-quality`)
- **Platform**: Ubuntu Latest
- **Python Version**: 3.11
- **Checks**:
  - **Black**: Code formatting validation
  - **isort**: Import sorting validation
  - **mypy**: Type checking (informational)
  - **bandit**: Security vulnerability scanning
  - **safety**: Dependency security checks
- **Artifacts**: Quality reports (bandit, safety)

### 3. Integration Job (`integration`)
- **Dependencies**: Waits for test and code-quality jobs
- **Validation**:
  - Complete workflow execution
  - Report file generation (JSON/Excel)
  - JSON structure validation
- **Artifacts**: Final monitoring reports (90-day retention)

### 4. Notification Job (`notify`)
- **Dependencies**: All other jobs
- **Features**:
  - Workflow summary generation
  - Job status reporting
  - Artifact listing

## Configuration Files

### pyproject.toml
Contains configuration for:
- **Black**: Line length 127, Python 3.8+ compatibility
- **isort**: Black-compatible import sorting
- **Coverage**: Source tracking and reporting exclusions

## Artifacts

The workflow generates several types of artifacts:

1. **Test Reports**: Per-platform/Python version test results
2. **Code Quality Reports**: Security and dependency analysis
3. **Final Reports**: Generated JSON/Excel monitoring reports

## Path Filtering

The workflow only runs when changes are made to:
- `ap2-monitor/**` (any file in the ap2-monitor directory)
- `.github/workflows/ap2-monitor.yml` (the workflow itself)

This ensures efficient CI/CD resource usage.

## Coverage Integration

The workflow integrates with Codecov for coverage reporting:
- Coverage data uploaded from Ubuntu + Python 3.11 combination
- Reports available in GitHub PR checks
- Configurable failure thresholds

## Manual Workflow Execution

To manually trigger the workflow:
1. Go to the repository on GitHub
2. Click "Actions" tab
3. Select "AP2 Monitor CI/CD" workflow
4. Click "Run workflow" button
5. Choose branch and click "Run workflow"

## Monitoring and Debugging

### Workflow Status
- View workflow status in the GitHub Actions tab
- Check individual job logs for detailed information
- Download artifacts for offline analysis

### Common Issues
- **Dependency Failures**: Check requirements.txt compatibility
- **Test Failures**: Review test logs in the test job
- **Quality Issues**: Check black/flake8 reports for formatting problems

## Maintenance

### Adding New Python Versions
Update the matrix in the test job:
```yaml
python-version: ['3.8', '3.9', '3.10', '3.11', '3.12', '3.13']
```

### Modifying Quality Checks
Add or remove tools in the code-quality job and update pyproject.toml accordingly.

### Artifact Retention
- Test artifacts: 30 days
- Quality reports: 30 days  
- Final reports: 90 days

Adjust retention-days values as needed for your organization's requirements.