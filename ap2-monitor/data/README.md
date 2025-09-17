# AP2 Monitoring Data

This directory contains the results from automated monitoring of GitHub repositories that implement or use the Agent Payments Protocol (AP2).

## File Types

- `ap2_monitoring_YYYYMMDD_HHMMSS.json` - Detailed analysis of each repository
- `summary_YYYYMMDD_HHMMSS.json` - Summary report with rating distribution
- `latest_results.json` - Most recent monitoring results (updated automatically)

## Sample Output

The monitoring system evaluates repositories on multiple criteria and provides ratings from 1-5 stars:

### Recent Findings (Demo Data)
- **ai-payments/ap2-core**: ⭐⭐⭐⭐⭐ (5/5) - Excellent AP2 implementation with comprehensive documentation
- **devtools/agent-payment-sdk**: ⭐⭐⭐⭐ (4/5) - Good AP2 integration, well documented, needs CI setup
- **examples/ap2-example**: ⭐⭐⭐ (3/5) - Basic AP2 implementation with adequate documentation

### Rating Distribution
- 5 stars: 33% (1 repo)
- 4 stars: 33% (1 repo)  
- 3 stars: 33% (1 repo)
- 2 stars: 0% (0 repos)
- 1 star: 0% (0 repos)

## Next Monitoring Run

The system runs automatically every 5 days. You can also trigger it manually via GitHub Actions.

*Last updated: Demo data generated on 2025-09-17*