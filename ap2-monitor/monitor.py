#!/usr/bin/env python3
"""
AP2 Repository Monitor
Monitors GitHub repositories that use Agent Payments Protocol (AP2) and rates them 1-5 stars.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from github import Github
from dataclasses import dataclass, asdict


@dataclass
class RepositoryRating:
    """Data class for repository rating information."""
    name: str
    full_name: str
    url: str
    description: str
    stars: int
    forks: int
    issues: int
    last_updated: str
    has_readme: bool
    has_license: bool
    has_ci: bool
    ap2_implementation_quality: int
    documentation_quality: int
    activity_score: int
    final_rating: int
    rating_date: str
    notes: str


class AP2Monitor:
    """Main class for monitoring AP2 repositories."""
    
    def __init__(self, github_token: str):
        """Initialize the monitor with GitHub API access."""
        self.github = Github(github_token)
        self.setup_logging()
        self.data_dir = "data"
        
    def setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ap2_monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def search_ap2_repositories(self) -> List[Dict]:
        """Search for repositories using Agent Payments Protocol."""
        search_terms = [
            "Agent Payments Protocol",
            "AP2 protocol",
            "agent payments",
            "autonomous payments",
            "ai agent payments"
        ]
        
        repositories = []
        self.logger.info("Starting AP2 repository search...")
        
        for term in search_terms:
            try:
                # Search in code, README, and description
                query = f'"{term}" in:readme,description,name'
                repos = self.github.search_repositories(query, sort="updated", order="desc")
                
                for repo in repos[:20]:  # Limit to top 20 results per search term
                    if repo.full_name not in [r['full_name'] for r in repositories]:
                        repositories.append({
                            'name': repo.name,
                            'full_name': repo.full_name,
                            'url': repo.html_url,
                            'description': repo.description or "",
                            'stars': repo.stargazers_count,
                            'forks': repo.forks_count,
                            'issues': repo.open_issues_count,
                            'last_updated': repo.updated_at.isoformat(),
                            'repo_object': repo
                        })
                        
            except Exception as e:
                self.logger.error(f"Error searching for '{term}': {e}")
                
        self.logger.info(f"Found {len(repositories)} unique repositories")
        return repositories
        
    def analyze_repository(self, repo_data: Dict) -> RepositoryRating:
        """Analyze a repository and generate a rating."""
        repo = repo_data['repo_object']
        
        # Check for README
        has_readme = self._has_readme(repo)
        
        # Check for license
        has_license = repo.license is not None
        
        # Check for CI/CD
        has_ci = self._has_ci_setup(repo)
        
        # Evaluate AP2 implementation quality (1-5)
        ap2_quality = self._evaluate_ap2_implementation(repo)
        
        # Evaluate documentation quality (1-5)
        doc_quality = self._evaluate_documentation(repo, has_readme)
        
        # Calculate activity score (1-5)
        activity_score = self._calculate_activity_score(repo)
        
        # Calculate final rating (1-5)
        final_rating = self._calculate_final_rating(
            ap2_quality, doc_quality, activity_score, 
            repo_data['stars'], has_license, has_ci
        )
        
        # Generate notes
        notes = self._generate_notes(repo, ap2_quality, doc_quality, activity_score)
        
        return RepositoryRating(
            name=repo_data['name'],
            full_name=repo_data['full_name'],
            url=repo_data['url'],
            description=repo_data['description'],
            stars=repo_data['stars'],
            forks=repo_data['forks'],
            issues=repo_data['issues'],
            last_updated=repo_data['last_updated'],
            has_readme=has_readme,
            has_license=has_license,
            has_ci=has_ci,
            ap2_implementation_quality=ap2_quality,
            documentation_quality=doc_quality,
            activity_score=activity_score,
            final_rating=final_rating,
            rating_date=datetime.now().isoformat(),
            notes=notes
        )
        
    def _has_readme(self, repo) -> bool:
        """Check if repository has a README file."""
        try:
            repo.get_readme()
            return True
        except:
            return False
            
    def _has_ci_setup(self, repo) -> bool:
        """Check if repository has CI/CD setup."""
        try:
            workflows = repo.get_workflows()
            return workflows.totalCount > 0
        except:
            return False
            
    def _evaluate_ap2_implementation(self, repo) -> int:
        """Evaluate the quality of AP2 implementation (1-5)."""
        score = 1
        
        try:
            # Check for specific AP2-related files and patterns
            contents = repo.get_contents("")
            files = [f.name.lower() for f in contents]
            
            # Look for agent-related files
            if any('agent' in f for f in files):
                score += 1
            if any('payment' in f for f in files):
                score += 1
            if any('protocol' in f for f in files):
                score += 1
                
            # Check for configuration files
            if any(f in files for f in ['config.json', 'config.yaml', 'settings.py']):
                score += 1
                
        except Exception as e:
            self.logger.debug(f"Error evaluating AP2 implementation for {repo.name}: {e}")
            
        return min(score, 5)
        
    def _evaluate_documentation(self, repo, has_readme: bool) -> int:
        """Evaluate documentation quality (1-5)."""
        score = 1
        
        if has_readme:
            score += 2
            
        try:
            # Check for additional documentation
            contents = repo.get_contents("")
            files = [f.name.lower() for f in contents]
            
            if 'docs' in [f for f in files]:
                score += 1
            if any(f.startswith('contributing') for f in files):
                score += 1
                
        except Exception as e:
            self.logger.debug(f"Error evaluating documentation for {repo.name}: {e}")
            
        return min(score, 5)
        
    def _calculate_activity_score(self, repo) -> int:
        """Calculate repository activity score (1-5)."""
        now = datetime.now()
        last_update = repo.updated_at
        days_since_update = (now - last_update).days
        
        if days_since_update <= 7:
            return 5
        elif days_since_update <= 30:
            return 4
        elif days_since_update <= 90:
            return 3
        elif days_since_update <= 365:
            return 2
        else:
            return 1
            
    def _calculate_final_rating(self, ap2_quality: int, doc_quality: int, 
                               activity_score: int, stars: int, has_license: bool, 
                               has_ci: bool) -> int:
        """Calculate the final rating (1-5)."""
        # Weighted average of different factors
        weights = {
            'ap2_quality': 0.4,
            'documentation': 0.2,
            'activity': 0.2,
            'community': 0.1,  # based on stars
            'best_practices': 0.1  # license + CI
        }
        
        # Normalize stars to 1-5 scale
        star_score = min(5, max(1, (stars // 10) + 1)) if stars > 0 else 1
        
        # Best practices score
        bp_score = 1
        if has_license:
            bp_score += 2
        if has_ci:
            bp_score += 2
            
        final_score = (
            weights['ap2_quality'] * ap2_quality +
            weights['documentation'] * doc_quality +
            weights['activity'] * activity_score +
            weights['community'] * star_score +
            weights['best_practices'] * bp_score
        )
        
        return max(1, min(5, round(final_score)))
        
    def _generate_notes(self, repo, ap2_quality: int, doc_quality: int, 
                       activity_score: int) -> str:
        """Generate descriptive notes for the rating."""
        notes = []
        
        if ap2_quality >= 4:
            notes.append("Strong AP2 implementation")
        elif ap2_quality <= 2:
            notes.append("Limited AP2 implementation evidence")
            
        if doc_quality >= 4:
            notes.append("Well documented")
        elif doc_quality <= 2:
            notes.append("Needs better documentation")
            
        if activity_score >= 4:
            notes.append("Recently active")
        elif activity_score <= 2:
            notes.append("Low activity")
            
        return "; ".join(notes) if notes else "Standard implementation"
        
    def save_results(self, ratings: List[RepositoryRating]):
        """Save monitoring results to JSON files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        detailed_file = f"{self.data_dir}/ap2_monitoring_{timestamp}.json"
        with open(detailed_file, 'w') as f:
            json.dump([asdict(rating) for rating in ratings], f, indent=2)
            
        # Save summary
        summary = {
            "monitoring_date": datetime.now().isoformat(),
            "total_repositories": len(ratings),
            "rating_distribution": {
                "5_stars": len([r for r in ratings if r.final_rating == 5]),
                "4_stars": len([r for r in ratings if r.final_rating == 4]),
                "3_stars": len([r for r in ratings if r.final_rating == 3]),
                "2_stars": len([r for r in ratings if r.final_rating == 2]),
                "1_star": len([r for r in ratings if r.final_rating == 1])
            },
            "top_rated": [
                {"name": r.full_name, "rating": r.final_rating, "url": r.url}
                for r in sorted(ratings, key=lambda x: x.final_rating, reverse=True)[:5]
            ]
        }
        
        summary_file = f"{self.data_dir}/summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
            
        # Update latest results
        latest_file = f"{self.data_dir}/latest_results.json"
        with open(latest_file, 'w') as f:
            json.dump([asdict(rating) for rating in ratings], f, indent=2)
            
        self.logger.info(f"Results saved to {detailed_file} and {summary_file}")
        
    def run_monitoring(self):
        """Run the complete monitoring process."""
        self.logger.info("Starting AP2 repository monitoring...")
        
        try:
            # Search for repositories
            repositories = self.search_ap2_repositories()
            
            if not repositories:
                self.logger.warning("No repositories found")
                return
                
            # Analyze and rate repositories
            ratings = []
            for repo_data in repositories:
                try:
                    rating = self.analyze_repository(repo_data)
                    ratings.append(rating)
                    self.logger.info(
                        f"Rated {rating.full_name}: {rating.final_rating}/5 stars"
                    )
                except Exception as e:
                    self.logger.error(f"Error analyzing {repo_data['full_name']}: {e}")
                    
            # Save results
            if ratings:
                self.save_results(ratings)
                self.logger.info(f"Monitoring completed. Analyzed {len(ratings)} repositories")
            else:
                self.logger.warning("No repositories were successfully analyzed")
                
        except Exception as e:
            self.logger.error(f"Monitoring failed: {e}")
            raise


def main():
    """Main entry point."""
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")
        
    monitor = AP2Monitor(github_token)
    monitor.run_monitoring()


if __name__ == "__main__":
    main()