import json
from dataclasses import dataclass, field
import pandas as pd
import os
from datetime import datetime

@dataclass
class RepositoryData:
    name: str
    rating: int
    url: str
    description: str = ""
    topics: list[str] = field(default_factory=list)
    language: str = ""
    stars: int = 0
    forks: int = 0

class AP2Monitor:
    def __init__(self):
        self.repositories = []

    def add_repository(self, repo: RepositoryData):
        self.repositories.append(repo)

    def generate_report(self) -> dict:
        self.repositories.sort(key=lambda r: r.rating, reverse=True)
        top_rated = [
            {
                "name": repo.name,
                "rating": repo.rating,
                "url": repo.url,
                "explanation": self._generate_explanation(repo),
                "dws_iq_suitable": self._assess_dws_iq_suitability(repo),
            }
            for repo in self.repositories
        ]
        return {"top_rated": top_rated}

    def generate_top_rated_report(self) -> list:
        """Return the list of top rated repositories (sorted)."""
        return self.generate_report()["top_rated"]

    def generate_json_report(self) -> str:
        """Return the full report as a JSON string."""
        return json.dumps({"top_rated": self.generate_top_rated_report()})

    def save_reports(self, base_dir: str | None = None):
        report = self.generate_report()

        results_dir = os.path.join(base_dir or ".", "Results")
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Filenames per requirement: Result<ddmmyyyy>.xlsx and Result<ddmmyyyy>.json
        date_str_dmy = datetime.now().strftime("%d%m%Y")
        excel_filename = f"Result{date_str_dmy}.xlsx"
        json_filename = f"Result{date_str_dmy}.json"

        # Save JSON report
        with open(os.path.join(results_dir, json_filename), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        # Save Excel report
        df = pd.DataFrame(report["top_rated"])
        df.to_excel(os.path.join(results_dir, excel_filename), index=False)

    def _generate_explanation(self, repo: RepositoryData) -> str:
        lang_map = {
            "Python": "versatile for data science, web development, and automation.",
            "Go": "excellent for high-performance, concurrent systems.",
            "JavaScript": "the language of the web, essential for front-end development.",
            "TypeScript": "a typed superset of JavaScript that enhances code quality.",
            "C#": "a powerful language for building Windows apps and enterprise systems.",
            "Java": "a robust, platform-independent language for large-scale applications.",
        }
        
        explanation = lang_map.get(repo.language, "a language with various applications.")

        # Topic-based cues
        ai_topics = {"ai", "machine-learning", "deep-learning"}
        cloud_topics = {"cloud", "kubernetes", "microservices"}
        topics_lower = {t.lower() for t in repo.topics}
        if topics_lower & ai_topics:
            explanation += " with focus on AI/ML"
        if topics_lower & cloud_topics:
            explanation += " suitable for cloud-native systems"

        # Popularity cues
        if repo.stars > 1000:
            explanation += " highly popular with strong community adoption"
        elif repo.stars > 100:
            explanation += " gaining popularity with a growing community"

        return f"{repo.language} - {explanation}"

    def _assess_dws_iq_suitability(self, repo: RepositoryData) -> bool:
        suitable_languages = ["Python", "Go", "JavaScript", "TypeScript", "C#", "Java"]
        relevant_topics = ["ai", "cloud", "microservices", "automation", "analytics"]

        if repo.language not in suitable_languages:
            return False

        if repo.stars < 10 or repo.rating < 3:
            return False

        # Either relevant topics OR description keywords should qualify
        if any(topic in repo.topics for topic in relevant_topics):
            return True

        description_keywords = ["intelligent", "digital", "workspace", "industry"]
        if any(keyword in repo.description.lower() for keyword in description_keywords):
            return True

        return False

# Example Usage
if __name__ == "__main__":
    monitor = AP2Monitor()

    # Add sample repositories
    monitor.add_repository(RepositoryData(name="wing", rating=5, url="https://github.com/winglang/wing", description="Compiler and SDK for a cloud-oriented programming language", topics=["cloud", "compiler", "typescript"], language="TypeScript", stars=1500, forks=100))
    monitor.add_repository(RepositoryData(name="fastapi", rating=5, url="https://github.com/tiangolo/fastapi", description="A modern, fast (high-performance) web framework for building APIs with Python 3.7+", topics=["python", "api", "web"], language="Python", stars=60000, forks=5000))
    monitor.add_repository(RepositoryData(name="temporal", rating=4, url="https://github.com/temporalio/temporal", description="A durable execution system for microservices", topics=["microservices", "go", "automation"], language="Go", stars=8000, forks=800))
    monitor.add_repository(RepositoryData(name="my-internal-project", rating=3, url="https://github.com/my-org/my-internal-project", description="An intelligent digital workspace solution", topics=["analytics", "csharp"], language="C#", stars=50, forks=10))

    # Save reports to Results/ directory
    monitor.save_reports()
    print("Reports generated successfully in the 'Results' directory.")
