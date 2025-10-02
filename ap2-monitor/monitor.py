#!/usr/bin/env python3
"""
AP2 Repository Monitoring Agent

This module monitors GitHub repositories and generates JSON reports
with repository ratings, analysis, and DWS IQ suitability assessments.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass

import pandas as pd

try:
    from github import Github
    from github.GithubException import GithubException
except ImportError:  # pragma: no cover
    Github = None  # type: ignore
    GithubException = Exception  # type: ignore


AI_TOPICS = [
    'machine-learning',
    'ai',
    'artificial-intelligence',
    'deep-learning',
    'tensorflow',
    'pytorch'
]

CLOUD_TOPICS = [
    'docker',
    'kubernetes',
    'cloud',
    'aws',
    'azure',
    'gcp',
    'terraform'
]

WEB_TOPICS = [
    'web',
    'frontend',
    'backend',
    'api',
    'rest',
    'graphql'
]

LANGUAGE_INSIGHTS = {
    'Python': 'versatile for data science, web development, and automation',
    'JavaScript': 'ideal for web applications and full-stack development',
    'Go': 'excellent for cloud-native and high-performance applications',
    'Java': 'robust for enterprise applications and microservices',
    'C#': 'powerful for .NET applications and enterprise solutions',
    'TypeScript': 'type-safe JavaScript for large-scale applications',
    'Rust': 'systems programming with memory safety and performance',
    'C++': 'high-performance applications and system programming'
}

DWS_RELEVANT_TOPICS = [
    'ai', 'machine-learning', 'data-science', 'cloud', 'kubernetes',
    'docker', 'microservices', 'api', 'monitoring', 'automation',
    'devops', 'infrastructure', 'security', 'analytics'
]

DWS_KEYWORDS = [
    'intelligent', 'digital', 'workspace', 'industry', 'automation',
    'analytics', 'monitoring', 'cloud', 'enterprise', 'platform'
]

DEFAULT_KEYWORDS = sorted({
    *AI_TOPICS,
    *CLOUD_TOPICS,
    *WEB_TOPICS,
    *DWS_RELEVANT_TOPICS,
    *DWS_KEYWORDS,
})


@dataclass
class RepositoryData:
    """Data class for repository information"""
    name: str
    rating: int
    url: str
    description: str = ""
    topics: List[str] = None
    language: str = ""
    stars: int = 0
    forks: int = 0
    
    def __post_init__(self):
        if self.topics is None:
            self.topics = []


class AP2Monitor:
    """AP2 Repository Monitoring Agent"""
    
    def __init__(self, github_token: Optional[str] = None):
        self.repositories: List[RepositoryData] = []
        self.github_token = github_token or os.getenv("AP2_GITHUB_TOKEN")
        self.github_client = None
        if Github:
            try:
                if self.github_token:
                    self.github_client = Github(self.github_token)
                else:
                    self.github_client = Github()
            except GithubException as exc:  # pragma: no cover
                print(f"Failed to initialize GitHub client: {exc}")
                self.github_client = None
        
    def add_repository(self, repo_data: RepositoryData):
        """Add a repository to be monitored"""
        self.repositories.append(repo_data)

    def fetch_repositories(self, keywords: Optional[List[str]] = None, per_keyword_limit: int = 10) -> None:
        """Fetch repositories from GitHub matching the provided keywords."""
        if not Github:
            raise RuntimeError("PyGithub is required to use GitHub search. Install dependencies.")
        if not self.github_client:
            raise RuntimeError("GitHub client is not initialized. Provide a token or ensure PyGithub is installed.")

        keywords = keywords or DEFAULT_KEYWORDS

        seen_urls = {repo.url for repo in self.repositories}

        for keyword in keywords:
            try:
                query = f"{keyword} in:name,description,topics"
                search_results = self.github_client.search_repositories(query=query, sort="stars", order="desc")
                for repo in search_results[:per_keyword_limit]:
                    url = repo.html_url
                    if url in seen_urls:
                        continue

                    topics = list(self._extract_topics(repo))
                    repo_data = RepositoryData(
                        name=repo.full_name,
                        rating=min(5, max(1, int(repo.stargazers_count / 500) + 1)),
                        url=url,
                        description=repo.description or "",
                        topics=topics,
                        language=repo.language or "",
                        stars=repo.stargazers_count,
                        forks=repo.forks_count
                    )
                    self.add_repository(repo_data)
                    seen_urls.add(url)
            except GithubException as exc:  # pragma: no cover
                print(f"GitHub API error for keyword '{keyword}': {exc}")
    
    @staticmethod
    def _extract_topics(repo: Any) -> Set[str]:
        topics: Set[str] = set()
        raw_topics = getattr(repo, 'topics', None)
        if isinstance(raw_topics, list):
            topics.update(str(topic).lower() for topic in raw_topics)
        elif raw_topics:
            try:
                topics.update(str(topic.name).lower() for topic in raw_topics())
            except TypeError:
                topics.update(str(topic).lower() for topic in raw_topics)
        return topics

    def _generate_explanation(self, repo: RepositoryData) -> str:
        """
        Generate automated analysis of repository usage
        
        Args:
            repo: Repository data object
            
        Returns:
            Short explanation string
        """
        explanations = []
        topics_lower = self._extract_topics(repo)

        if topics_lower.intersection({topic.lower() for topic in AI_TOPICS}):
            explanations.append("AI/ML capabilities for intelligent applications")
        if topics_lower.intersection({topic.lower() for topic in CLOUD_TOPICS}):
            explanations.append("cloud-native technologies suitable for modern infrastructure")
        if topics_lower.intersection({topic.lower() for topic in WEB_TOPICS}):
            explanations.append("web development focused with modern frameworks")
        
        # Analyze by programming language
        if repo.language and len(explanations) < 2:
            if repo.language in LANGUAGE_INSIGHTS:
                explanations.append(f"{repo.language} - {LANGUAGE_INSIGHTS[repo.language]}")
        
        # Analyze by popularity
        if len(explanations) < 2:
            if repo.stars > 1000:
                explanations.append("highly popular with strong community adoption")
            elif repo.stars > 100:
                explanations.append("growing popularity with active community")
        
        # Analyze by activity (based on forks)
        if len(explanations) < 2:
            if repo.forks > 500:
                explanations.append("actively forked indicating collaborative development")
            elif repo.forks > 50:
                explanations.append("moderate forking activity showing developer interest")
        
        # Default explanation if no specific patterns found
        if not explanations:
            explanations.append("general-purpose repository with standard development practices")
            
        return ". ".join(explanations[:2])  # Limit to 2 main points for brevity
    
    def _assess_dws_iq_suitability(self, repo: RepositoryData) -> bool:
        """
        Assess if repository is suitable for DWS IQ repository
        
        This is placeholder logic that can be easily customized by the user
        to match their specific DWS IQ criteria.
        
        Args:
            repo: Repository data object
            
        Returns:
            Boolean indicating suitability
        """
        # Placeholder criteria - easily customizable
        suitable_criteria = []
        
        # Criterion 1: Language suitability
        dws_languages = ['Python', 'Go', 'JavaScript', 'TypeScript', 'C#', 'Java']
        if repo.language in dws_languages:
            suitable_criteria.append(True)
        
        # Criterion 2: Topic relevance
        topics_lower = (
            {topic.lower() for topic in repo.topics}
            if isinstance(repo, RepositoryData)
            else self._extract_topics(repo)
        )
        if topics_lower.intersection({topic.lower() for topic in DWS_RELEVANT_TOPICS}):
            suitable_criteria.append(True)
            
        # Criterion 3: Minimum quality threshold
        if repo.stars >= 10 and repo.rating >= 3:
            suitable_criteria.append(True)
            
        # Criterion 4: Description keywords (if available)
        if repo.description:
            description_lower = repo.description.lower()
            if any(keyword in description_lower for keyword in DWS_KEYWORDS):
                suitable_criteria.append(True)
        
        # Repository is suitable if it meets at least 2 criteria
        return len(suitable_criteria) >= 2
    
    def generate_top_rated_report(self) -> List[Dict[str, Any]]:
        """
        Generate JSON report for top-rated repositories
        
        Returns:
            List of repository dictionaries with enhanced fields
        """
        # Sort repositories by rating (descending)
        sorted_repos = sorted(self.repositories, key=lambda x: x.rating, reverse=True)
        
        report = []
        for repo in sorted_repos:
            repo_entry = {
                "name": repo.name,
                "rating": repo.rating,
                "url": repo.url,
                "explanation": self._generate_explanation(repo),
                "dws_iq_suitable": self._assess_dws_iq_suitability(repo)
            }
            report.append(repo_entry)
            
        return report
    
    def generate_json_report(self, indent: int = 2) -> str:
        """
        Generate formatted JSON report
        
        Args:
            indent: JSON indentation level
            
        Returns:
            Formatted JSON string
        """
        report = {
            "top_rated": self.generate_top_rated_report()
        }
        return json.dumps(report, indent=indent)
    
    def save_reports(self, base_path: str = ".") -> None:
        """
        Save reports to JSON and Excel files in Results directory
        
        Args:
            base_path: Base directory path (defaults to current directory)
        """
        # Create Results directory if it doesn't exist
        results_dir = os.path.join(base_path, "Results")
        os.makedirs(results_dir, exist_ok=True)
        
        # Generate report data
        report_data = self.generate_top_rated_report()
        now = datetime.now()
        timestamp_str = now.strftime("%H%d%m%Y")

        # Save JSON report
        json_report = {
            "top_rated": report_data
        }
        json_file_path = os.path.join(results_dir, "report.json")
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2, ensure_ascii=False)
        print(f"JSON report saved to: {json_file_path}")

        dated_json_path = os.path.join(results_dir, f"report_{timestamp_str}.json")
        with open(dated_json_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2, ensure_ascii=False)
        print(f"JSON report saved to: {dated_json_path}")
        
        # Save Excel report
        if report_data:
            # Convert to DataFrame for Excel export
            df = pd.DataFrame(report_data)

            excel_file_path = os.path.join(results_dir, "report.xlsx")
            df.to_excel(excel_file_path, index=False, engine='openpyxl')
            print(f"Excel report saved to: {excel_file_path}")

            dated_excel_path = os.path.join(results_dir, f"report_{timestamp_str}.xlsx")
            df.to_excel(dated_excel_path, index=False, engine='openpyxl')
            print(f"Excel report saved to: {dated_excel_path}")

            results_excel_path = os.path.join(results_dir, f"results{timestamp_str}.xlsx")
            df.to_excel(results_excel_path, index=False, engine='openpyxl')
            print(f"Excel report saved to: {results_excel_path}")
        else:
            print("No data to save to Excel file")


def main():
    """Example usage of the AP2 Monitor"""
    monitor = AP2Monitor()
    
    # Example repositories for demonstration
    example_repos = [
        RepositoryData(
            name="awesome-python",
            rating=5,
            url="https://github.com/vinta/awesome-python",
            description="A curated list of awesome Python frameworks, libraries, software and resources",
            topics=['python', 'awesome-list', 'resources'],
            language="Python",
            stars=2500,
            forks=400
        ),
        RepositoryData(
            name="kubernetes",
            rating=5,
            url="https://github.com/kubernetes/kubernetes",
            description="Production-Grade Container Scheduling and Management",
            topics=['kubernetes', 'containers', 'orchestration', 'cloud'],
            language="Go",
            stars=15000,
            forks=8000
        ),
        RepositoryData(
            name="small-project",
            rating=3,
            url="https://github.com/example/small-project",
            description="A small utility project",
            topics=['utility'],
            language="JavaScript",
            stars=5,
            forks=1
        )
    ]
    
    for repo in example_repos:
        monitor.add_repository(repo)
    
    # Save the report to files instead of printing
    monitor.save_reports()


if __name__ == "__main__":
    main()