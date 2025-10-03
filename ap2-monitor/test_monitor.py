#!/usr/bin/env python3
"""
Test suite for AP2 Repository Monitoring Agent

This module contains comprehensive tests for the monitor.py functionality,
including tests for the new explanation and dws_iq_suitable fields.
"""

import unittest
import json
from unittest.mock import Mock, patch
import sys
import os
from datetime import datetime
import pandas as pd

# Add the ap2-monitor directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from monitor import AP2Monitor, RepositoryData


class TestRepositoryData(unittest.TestCase):
    """Test cases for RepositoryData class"""
    
    def test_repository_data_creation(self):
        """Test creating a RepositoryData instance"""
        repo = RepositoryData(
            name="test-repo",
            rating=4,
            url="https://github.com/test/test-repo"
        )
        
        self.assertEqual(repo.name, "test-repo")
        self.assertEqual(repo.rating, 4)
        self.assertEqual(repo.url, "https://github.com/test/test-repo")
        self.assertEqual(repo.topics, [])
        
    def test_repository_data_with_topics(self):
        """Test creating a RepositoryData instance with topics"""
        repo = RepositoryData(
            name="test-repo",
            rating=5,
            url="https://github.com/test/test-repo",
            topics=['python', 'machine-learning']
        )
        
        self.assertEqual(repo.topics, ['python', 'machine-learning'])


class TestAP2Monitor(unittest.TestCase):
    """Test cases for AP2Monitor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.monitor = AP2Monitor()
        
        # Create test repositories
        self.python_repo = RepositoryData(
            name="python-ml",
            rating=5,
            url="https://github.com/example/python-ml",
            description="Machine learning library for Python applications",
            topics=['python', 'machine-learning', 'ai'],
            language="Python",
            stars=1500,
            forks=300
        )
        
        self.go_repo = RepositoryData(
            name="cloud-service",
            rating=4,
            url="https://github.com/example/cloud-service",
            description="Cloud-native microservice platform",
            topics=['go', 'cloud', 'kubernetes', 'microservices'],
            language="Go",
            stars=800,
            forks=150
        )
        
        self.small_repo = RepositoryData(
            name="simple-util",
            rating=2,
            url="https://github.com/example/simple-util",
            description="Simple utility functions",
            topics=['utility'],
            language="JavaScript",
            stars=5,
            forks=1
        )
        
    def test_add_repository(self):
        """Test adding repositories to monitor"""
        self.monitor.add_repository(self.python_repo)
        self.assertEqual(len(self.monitor.repositories), 1)
        self.assertEqual(self.monitor.repositories[0].name, "python-ml")
        
    def test_generate_explanation_python(self):
        """Test explanation generation for Python repository"""
        explanation = self.monitor._generate_explanation(self.python_repo)
        
        self.assertIn("Python", explanation)
        self.assertIn("data science", explanation)
        self.assertTrue(len(explanation) > 0)
        
    def test_generate_explanation_go(self):
        """Test explanation generation for Go repository"""
        explanation = self.monitor._generate_explanation(self.go_repo)
        
        self.assertIn("Go", explanation)
        self.assertIn("cloud-native", explanation)
        
    def test_generate_explanation_popularity(self):
        """Test explanation includes popularity analysis"""
        # Create a repo without specific topics so popularity shows
        popular_repo = RepositoryData(
            name="popular-util",
            rating=4,
            url="https://github.com/example/popular-util",
            description="Popular utility library",
            topics=['utility'],  # Non-specific topic
            language="JavaScript",
            stars=1500,
            forks=300
        )
        
        explanation = self.monitor._generate_explanation(popular_repo)
        self.assertIn("popular", explanation)
        
    def test_generate_explanation_topics(self):
        """Test explanation includes topic analysis"""
        explanation = self.monitor._generate_explanation(self.python_repo)
        # Check that the explanation mentions either the language or some relevant content
        self.assertTrue(
            "AI/ML" in explanation or 
            "data science" in explanation or 
            "machine learning" in explanation or
            "popular" in explanation
        )
        
    def test_generate_explanation_ai_topics(self):
        """Test explanation for AI-focused repository"""
        ai_repo = RepositoryData(
            name="ai-toolkit",
            rating=4,
            url="https://github.com/example/ai-toolkit",
            description="AI and machine learning toolkit",
            topics=['machine-learning', 'ai', 'deep-learning'],
            language="Python",
            stars=500,
            forks=100
        )
        
        explanation = self.monitor._generate_explanation(ai_repo)
        self.assertIn("AI/ML", explanation)
        
    def test_assess_dws_iq_suitability_suitable(self):
        """Test DWS IQ suitability assessment for suitable repository"""
        is_suitable = self.monitor._assess_dws_iq_suitability(self.python_repo)
        self.assertTrue(is_suitable)
        
    def test_assess_dws_iq_suitability_cloud(self):
        """Test DWS IQ suitability for cloud repository"""
        is_suitable = self.monitor._assess_dws_iq_suitability(self.go_repo)
        self.assertTrue(is_suitable)
        
    def test_assess_dws_iq_suitability_not_suitable(self):
        """Test DWS IQ suitability assessment for unsuitable repository"""
        is_suitable = self.monitor._assess_dws_iq_suitability(self.small_repo)
        self.assertFalse(is_suitable)
        
    def test_generate_top_rated_report_structure(self):
        """Test the structure of generated top-rated report"""
        self.monitor.add_repository(self.python_repo)
        self.monitor.add_repository(self.go_repo)
        
        report = self.monitor.generate_top_rated_report()
        
        self.assertEqual(len(report), 2)
        
        # Check first repository (highest rated)
        first_repo = report[0]
        self.assertEqual(first_repo["name"], "python-ml")
        self.assertEqual(first_repo["rating"], 5)
        self.assertEqual(first_repo["url"], "https://github.com/example/python-ml")
        self.assertIn("explanation", first_repo)
        self.assertIn("dws_iq_suitable", first_repo)
        self.assertIsInstance(first_repo["explanation"], str)
        self.assertIsInstance(first_repo["dws_iq_suitable"], bool)
        
    def test_generate_top_rated_report_sorting(self):
        """Test that repositories are sorted by rating"""
        self.monitor.add_repository(self.go_repo)  # rating 4
        self.monitor.add_repository(self.python_repo)  # rating 5
        self.monitor.add_repository(self.small_repo)  # rating 2
        
        report = self.monitor.generate_top_rated_report()
        
        # Should be sorted by rating descending
        self.assertEqual(report[0]["rating"], 5)  # python-ml
        self.assertEqual(report[1]["rating"], 4)  # cloud-service
        self.assertEqual(report[2]["rating"], 2)  # simple-util
        
    def test_generate_json_report_format(self):
        """Test JSON report generation and format"""
        self.monitor.add_repository(self.python_repo)
        
        json_report = self.monitor.generate_json_report()
        
        # Verify it's valid JSON
        parsed_report = json.loads(json_report)
        
        # Check structure
        self.assertIn("top_rated", parsed_report)
        self.assertIsInstance(parsed_report["top_rated"], list)
        
        # Check first repository
        if parsed_report["top_rated"]:
            repo = parsed_report["top_rated"][0]
            required_fields = ["name", "rating", "url", "explanation", "dws_iq_suitable"]
            for field in required_fields:
                self.assertIn(field, repo)
                
    def test_original_fields_preserved(self):
        """Test that original fields are preserved in new format"""
        self.monitor.add_repository(self.python_repo)
        
        report = self.monitor.generate_top_rated_report()
        repo = report[0]
        
        # Original fields should be present
        self.assertEqual(repo["name"], "python-ml")
        self.assertEqual(repo["rating"], 5)
        self.assertEqual(repo["url"], "https://github.com/example/python-ml")
        
        # New fields should be present
        self.assertIn("explanation", repo)
        self.assertIn("dws_iq_suitable", repo)
        
    def test_empty_repository_list(self):
        """Test behavior with empty repository list"""
        report = self.monitor.generate_top_rated_report()
        self.assertEqual(report, [])
        
        json_report = self.monitor.generate_json_report()
        parsed_report = json.loads(json_report)
        self.assertEqual(parsed_report["top_rated"], [])
        
    def test_explanation_length_reasonable(self):
        """Test that explanations are reasonable length"""
        explanation = self.monitor._generate_explanation(self.python_repo)
        
        # Should be informative but not too long
        self.assertGreater(len(explanation), 10)
        self.assertLess(len(explanation), 300)
        
    def test_dws_iq_criteria_customizable(self):
        """Test that DWS IQ criteria can be easily identified for customization"""
        # This test ensures the structure is in place for easy customization
        
        # Create a repository that would be borderline
        borderline_repo = RepositoryData(
            name="test-repo",
            rating=3,
            url="https://github.com/test/test-repo",
            description="Test repository for intelligent digital workspace applications",
            topics=['test'],
            language="Python",
            stars=15,
            forks=2
        )
        
        # Should be suitable due to description keywords
        is_suitable = self.monitor._assess_dws_iq_suitability(borderline_repo)
        self.assertTrue(is_suitable)

    @patch('monitor.GithubException', new=Exception)
    @patch('monitor.Github')
    def test_fetch_repositories_with_keywords(self, mock_github):
        """Test GitHub keyword search adds repositories"""
        mock_client = Mock()
        mock_repo = Mock()
        mock_repo.html_url = "https://github.com/example/cloud-repo"
        mock_repo.full_name = "example/cloud-repo"
        mock_repo.description = "Cloud automation tools"
        mock_repo.topics = ['cloud', 'automation']
        mock_repo.language = 'Python'
        mock_repo.stargazers_count = 1200
        mock_repo.forks_count = 320

        mock_client.search_repositories.return_value = [mock_repo]
        mock_github.return_value = mock_client

        monitor = AP2Monitor(github_token="fake-token")
        monitor.fetch_repositories(['cloud'], per_keyword_limit=1)

        self.assertEqual(len(monitor.repositories), 1)
        fetched_repo = monitor.repositories[0]
        self.assertEqual(fetched_repo.name, "example/cloud-repo")
        self.assertEqual(fetched_repo.url, "https://github.com/example/cloud-repo")
        self.assertEqual(fetched_repo.rating, 3)
        self.assertEqual(fetched_repo.language, 'Python')
        self.assertEqual(fetched_repo.stars, 1200)
        self.assertEqual(fetched_repo.forks, 320)
        self.assertTrue(set(fetched_repo.topics).issuperset({'cloud', 'automation'}))
        mock_client.search_repositories.assert_called_with(
            query='cloud in:name,description,topics',
            sort='stars',
            order='desc'
        )

    @patch('monitor.DEFAULT_KEYWORDS', ['ai'])
    @patch('monitor.GithubException', new=Exception)
    @patch('monitor.Github')
    def test_fetch_repositories_uses_default_keywords(self, mock_github):
        """Test fetch_repositories uses default keyword list when none provided"""
        mock_client = Mock()
        mock_repo = Mock()
        mock_repo.html_url = "https://github.com/example/ai-repo"
        mock_repo.full_name = "example/ai-repo"
        mock_repo.description = "AI toolkit"
        mock_repo.topics = ['ai']
        mock_repo.language = 'Python'
        mock_repo.stargazers_count = 50
        mock_repo.forks_count = 5

        mock_client.search_repositories.return_value = [mock_repo]
        mock_github.return_value = mock_client

        monitor = AP2Monitor(github_token="fake-token")
        monitor.fetch_repositories(per_keyword_limit=1)

        self.assertEqual(len(monitor.repositories), 1)
        mock_client.search_repositories.assert_called_with(
            query='ai in:name,description,topics',
            sort='stars',
            order='desc'
        )

    def test_fetch_repositories_without_client_raises(self):
        """Test fetch_repositories raises when GitHub client unavailable"""
        monitor = AP2Monitor()
        monitor.github_client = None
        with self.assertRaises(RuntimeError):
            monitor.fetch_repositories(['cloud'])


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow"""
    
    def test_complete_workflow(self):
        """Test the complete monitoring workflow"""
        monitor = AP2Monitor()
        
        # Add multiple repositories
        repos = [
            RepositoryData(
                name="ai-platform",
                rating=5,
                url="https://github.com/company/ai-platform",
                description="Intelligent AI platform for digital workspace automation",
                topics=['ai', 'platform', 'automation'],
                language="Python",
                stars=2000,
                forks=500
            ),
            RepositoryData(
                name="legacy-tool",
                rating=2,
                url="https://github.com/old/legacy-tool",
                description="Old legacy tool",
                topics=['legacy'],
                language="C",
                stars=3,
                forks=0
            )
        ]
        
        for repo in repos:
            monitor.add_repository(repo)
            
        # Generate report
        json_report = monitor.generate_json_report()
        parsed_report = json.loads(json_report)
        
        # Verify structure and content
        self.assertIn("top_rated", parsed_report)
        top_rated = parsed_report["top_rated"]
        
        self.assertEqual(len(top_rated), 2)
        
        # First should be AI platform (higher rating)
        first_repo = top_rated[0]
        self.assertEqual(first_repo["name"], "ai-platform")
        self.assertEqual(first_repo["rating"], 5)
        self.assertTrue(first_repo["dws_iq_suitable"])
        self.assertIn("Python", first_repo["explanation"])
        
        # Second should be legacy tool (lower rating)
        second_repo = top_rated[1]
        self.assertEqual(second_repo["name"], "legacy-tool")
        self.assertEqual(second_repo["rating"], 2)
        self.assertFalse(second_repo["dws_iq_suitable"])

class TestFileSaving(unittest.TestCase):
    """Test cases for file saving functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.monitor = AP2Monitor()
        self.test_repo = RepositoryData(
            name="test-repo",
            rating=4,
            url="https://github.com/test/test-repo",
            description="A test repository for file saving",
            topics=['test', 'python'],
            language="Python",
            stars=100,
            forks=20
        )
        self.monitor.add_repository(self.test_repo)
        
        # Clean up any existing test files
        self.test_dir = "/tmp/test_results"
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir)
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir)
    
    @patch('monitor.datetime')
    def test_save_reports_creates_directory(self, mock_datetime):
        """Test that save_reports creates Results directory"""
        mock_datetime.now.return_value.strftime.return_value = '0815012025'
        self.monitor.save_reports(self.test_dir)
        
        results_dir = os.path.join(self.test_dir, "Results")
        self.assertTrue(os.path.exists(results_dir))
        self.assertTrue(os.path.isdir(results_dir))
    
    @patch('monitor.datetime')
    def test_save_reports_creates_json_file(self, mock_datetime):
        """Test that save_reports creates JSON file with correct content"""
        mock_datetime.now.return_value.strftime.return_value = '0815012025'
        self.monitor.save_reports(self.test_dir)
        
        date_str = datetime.now().strftime("%d%m%Y")
        json_file = os.path.join(self.test_dir, "Results", f"Result{date_str}.json")
        self.assertTrue(os.path.exists(json_file))
        
        # Verify JSON content
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIn("top_rated", data)
        self.assertEqual(len(data["top_rated"]), 1)
        self.assertEqual(data["top_rated"][0]["name"], "test-repo")

        dated_json = os.path.join(self.test_dir, "Results", "report_0815012025.json")
        self.assertTrue(os.path.exists(dated_json))
    
    @patch('monitor.datetime')
    def test_save_reports_creates_excel_file(self, mock_datetime):
        """Test that save_reports creates Excel file with correct content"""
        mock_datetime.now.return_value.strftime.return_value = '0815012025'
        self.monitor.save_reports(self.test_dir)
        
        date_str = datetime.now().strftime("%d%m%Y")
        excel_file = os.path.join(self.test_dir, "Results", f"Result{date_str}.xlsx")
        self.assertTrue(os.path.exists(excel_file))
        
        # Verify Excel content using pandas
        df = pd.read_excel(excel_file, engine='openpyxl')
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['name'], "test-repo")
        self.assertEqual(df.iloc[0]['rating'], 4)

        dated_excel = os.path.join(self.test_dir, "Results", "report_0815012025.xlsx")
        self.assertTrue(os.path.exists(dated_excel))

        results_excel = os.path.join(self.test_dir, "Results", "results0815012025.xlsx")
        self.assertTrue(os.path.exists(results_excel))


if __name__ == "__main__":
    unittest.main()