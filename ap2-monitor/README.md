# AP2 Repository Monitor

This system monitors GitHub repositories that implement or use the Agent Payments Protocol (AP2) and provides automated ratings from 1 to 5 stars.

## Features

- **Automated Repository Discovery**: Searches GitHub for repositories related to Agent Payments Protocol
- **Comprehensive Rating System**: Evaluates repositories based on multiple criteria:
  - AP2 implementation quality (40% weight)
  - Documentation quality (20% weight)
  - Repository activity (20% weight)
  - Community engagement (10% weight - based on stars)
  - Best practices (10% weight - license, CI/CD)
- **Scheduled Monitoring**: Runs automatically every 5 days via GitHub Actions
- **Historical Tracking**: Maintains records of ratings over time
- **Detailed Reports**: Generates comprehensive analysis and summary reports

## Rating Criteria

### 5 Stars ⭐⭐⭐⭐⭐
- Excellent AP2 implementation with clear evidence
- Comprehensive documentation with examples
- Active development (updated within last week)
- Strong community engagement (many stars/forks)
- Follows best practices (license, CI/CD)

### 4 Stars ⭐⭐⭐⭐
- Good AP2 implementation
- Well-documented with README
- Regular updates (within last month)
- Good community engagement
- Most best practices followed

### 3 Stars ⭐⭐⭐
- Basic AP2 implementation
- Adequate documentation
- Moderate activity (within last 3 months)
- Some community engagement
- Some best practices

### 2 Stars ⭐⭐
- Limited AP2 implementation evidence
- Minimal documentation
- Low activity (within last year)
- Little community engagement
- Few best practices

### 1 Star ⭐
- No clear AP2 implementation
- Poor or no documentation
- Inactive (over a year old)
- No community engagement
- No best practices

## Files Structure

```
ap2-monitor/
├── monitor.py              # Main monitoring script
├── requirements.txt        # Python dependencies
├── data/                   # Results storage
│   ├── latest_results.json # Most recent monitoring results
│   ├── summary_*.json      # Summary reports by date
│   └── ap2_monitoring_*.json # Detailed results by date
└── README.md              # This file
```

## Usage

### Manual Run
```bash
cd ap2-monitor
export GITHUB_TOKEN="your_github_token"
python monitor.py
```

### Automated Run
The system runs automatically every 5 days via GitHub Actions. Results are committed back to the repository.

## Output

The monitor generates several types of output:

1. **Detailed Results**: Complete analysis of each repository
2. **Summary Reports**: Overview with rating distribution and top repositories
3. **Logs**: Detailed logging of the monitoring process

## Configuration

The monitoring can be customized by modifying:
- Search terms in `search_ap2_repositories()`
- Rating weights in `_calculate_final_rating()`
- Evaluation criteria in the various `_evaluate_*()` methods

## Dependencies

- `requests`: HTTP library for API calls
- `PyGithub`: GitHub API wrapper
- `python-dateutil`: Date/time utilities

## License

This monitoring system is part of the blogtheristo repository and follows its licensing terms.