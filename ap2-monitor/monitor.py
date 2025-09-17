#!/usr/bin/env python3
"""
AP2 Repository Monitoring Agent

This module monitors GitHub repositories and generates JSON reports
with repository ratings, analysis, and DWS IQ suitability assessments.
"""

import json
import re
from typing import Dict, List, Any
from dataclasses import dataclass


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
    
    def __init__(self):
        self.repositories = []
        
    def add_repository(self, repo_data: RepositoryData):
        """Add a repository to be monitored"""
        self.repositories.append(repo_data)
    
    def _generate_explanation(self, repo: RepositoryData) -> str:
        """
        Generate automated analysis of repository usage
        
        Args:
            repo: Repository data object
            
        Returns:
            Short explanation string
        """
        explanations = []
        
        # Analyze by topics first (highest priority)
        cloud_topics = ['docker', 'kubernetes', 'cloud', 'aws', 'azure', 'gcp', 'terraform']
        ai_topics = ['machine-learning', 'ai', 'artificial-intelligence', 'deep-learning', 'tensorflow', 'pytorch']
        web_topics = ['web', 'frontend', 'backend', 'api', 'rest', 'graphql']
        
        if any(topic in repo.topics for topic in ai_topics):
            explanations.append("AI/ML capabilities for intelligent applications")
        if any(topic in repo.topics for topic in cloud_topics):
            explanations.append("cloud-native technologies suitable for modern infrastructure")
        if any(topic in repo.topics for topic in web_topics):
            explanations.append("web development focused with modern frameworks")
        
        # Analyze by programming language
        if repo.language and len(explanations) < 2:
            lang_insights = {
                'Python': 'versatile for data science, web development, and automation',
                'JavaScript': 'ideal for web applications and full-stack development', 
                'Go': 'excellent for cloud-native and high-performance applications',
                'Java': 'robust for enterprise applications and microservices',
                'C#': 'powerful for .NET applications and enterprise solutions',
                'TypeScript': 'type-safe JavaScript for large-scale applications',
                'Rust': 'systems programming with memory safety and performance',
                'C++': 'high-performance applications and system programming'
            }
            if repo.language in lang_insights:
                explanations.append(f"{repo.language} - {lang_insights[repo.language]}")
        
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
        dws_relevant_topics = [
            'ai', 'machine-learning', 'data-science', 'cloud', 'kubernetes', 
            'docker', 'microservices', 'api', 'monitoring', 'automation',
            'devops', 'infrastructure', 'security', 'analytics'
        ]
        if any(topic in repo.topics for topic in dws_relevant_topics):
            suitable_criteria.append(True)
            
        # Criterion 3: Minimum quality threshold
        if repo.stars >= 10 and repo.rating >= 3:
            suitable_criteria.append(True)
            
        # Criterion 4: Description keywords (if available)
        if repo.description:
            dws_keywords = [
                'intelligent', 'digital', 'workspace', 'industry', 'automation',
                'analytics', 'monitoring', 'cloud', 'enterprise', 'platform'
            ]
            description_lower = repo.description.lower()
            if any(keyword in description_lower for keyword in dws_keywords):
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
    
    # Generate and print the report
    print(monitor.generate_json_report())


if __name__ == "__main__":
    main()