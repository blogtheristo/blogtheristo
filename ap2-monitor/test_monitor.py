#!/usr/bin/env python3
"""
Test script for AP2 Monitor
Validates the monitoring system without making actual GitHub API calls.
"""

import json
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from monitor import AP2Monitor, RepositoryRating


def test_rating_calculation():
    """Test the rating calculation logic."""
    print("Testing rating calculation...")
    
    # Create a mock monitor (without GitHub token for testing)
    class MockMonitor(AP2Monitor):
        def __init__(self):
            self.data_dir = "data"
            
    monitor = MockMonitor()
    
    # Test cases for rating calculation
    test_cases = [
        {
            "name": "High Quality Repository",
            "ap2_quality": 5,
            "doc_quality": 5,
            "activity_score": 5,
            "stars": 100,
            "has_license": True,
            "has_ci": True,
            "expected": 5
        },
        {
            "name": "Medium Quality Repository", 
            "ap2_quality": 3,
            "doc_quality": 3,
            "activity_score": 3,
            "stars": 20,
            "has_license": True,
            "has_ci": False,
            "expected": 3
        },
        {
            "name": "Low Quality Repository",
            "ap2_quality": 1,
            "doc_quality": 1,
            "activity_score": 1,
            "stars": 0,
            "has_license": False,
            "has_ci": False,
            "expected": 1
        }
    ]
    
    for test_case in test_cases:
        rating = monitor._calculate_final_rating(
            test_case["ap2_quality"],
            test_case["doc_quality"],
            test_case["activity_score"],
            test_case["stars"],
            test_case["has_license"],
            test_case["has_ci"]
        )
        
        print(f"  {test_case['name']}: {rating}/5 (expected: {test_case['expected']}/5)")
        
        if abs(rating - test_case["expected"]) <= 1:  # Allow 1 point tolerance
            print("    ✅ PASS")
        else:
            print("    ❌ FAIL")
            
    print()


def test_data_structures():
    """Test the data structures and serialization."""
    print("Testing data structures...")
    
    # Create a sample rating
    rating = RepositoryRating(
        name="test-repo",
        full_name="user/test-repo", 
        url="https://github.com/user/test-repo",
        description="A test repository for AP2",
        stars=50,
        forks=10,
        issues=5,
        last_updated="2024-01-15T10:00:00Z",
        has_readme=True,
        has_license=True,
        has_ci=True,
        ap2_implementation_quality=4,
        documentation_quality=4,
        activity_score=3,
        final_rating=4,
        rating_date=datetime.now().isoformat(),
        notes="Well implemented AP2 protocol; Good documentation"
    )
    
    # Test serialization
    try:
        from dataclasses import asdict
        rating_dict = asdict(rating)
        json_str = json.dumps(rating_dict, indent=2)
        
        # Test deserialization
        loaded_dict = json.loads(json_str)
        
        print("  ✅ Data structure serialization: PASS")
        print(f"  Sample rating: {rating.full_name} - {rating.final_rating}/5 stars")
        
    except Exception as e:
        print(f"  ❌ Data structure serialization: FAIL - {e}")
        
    print()


def test_file_operations():
    """Test file operations and directory structure."""
    print("Testing file operations...")
    
    # Check if data directory exists
    if os.path.exists("data"):
        print("  ✅ Data directory exists")
    else:
        print("  ⚠️  Data directory does not exist (will be created during run)")
        
    # Test if we can write to the directory
    try:
        test_file = "data/test_file.json"
        os.makedirs("data", exist_ok=True)
        
        with open(test_file, 'w') as f:
            json.dump({"test": "data"}, f)
            
        # Clean up
        os.remove(test_file)
        
        print("  ✅ File write operations: PASS")
        
    except Exception as e:
        print(f"  ❌ File write operations: FAIL - {e}")
        
    print()


def generate_mock_results():
    """Generate mock monitoring results for demonstration."""
    print("Generating mock monitoring results...")
    
    # Create sample repositories with different ratings
    mock_ratings = [
        RepositoryRating(
            name="ap2-core",
            full_name="ai-payments/ap2-core",
            url="https://github.com/ai-payments/ap2-core",
            description="Core implementation of Agent Payments Protocol v2",
            stars=150,
            forks=45,
            issues=8,
            last_updated="2024-01-10T15:30:00Z",
            has_readme=True,
            has_license=True,
            has_ci=True,
            ap2_implementation_quality=5,
            documentation_quality=5,
            activity_score=4,
            final_rating=5,
            rating_date=datetime.now().isoformat(),
            notes="Excellent AP2 implementation; Comprehensive documentation; Active development"
        ),
        RepositoryRating(
            name="agent-payment-sdk",
            full_name="devtools/agent-payment-sdk",
            url="https://github.com/devtools/agent-payment-sdk",
            description="SDK for integrating with Agent Payments Protocol",
            stars=75,
            forks=20,
            issues=12,
            last_updated="2024-01-08T09:15:00Z",
            has_readme=True,
            has_license=True,
            has_ci=False,
            ap2_implementation_quality=4,
            documentation_quality=4,
            activity_score=4,
            final_rating=4,
            rating_date=datetime.now().isoformat(),
            notes="Good AP2 integration; Well documented; Needs CI setup"
        ),
        RepositoryRating(
            name="ap2-example",
            full_name="examples/ap2-example",
            url="https://github.com/examples/ap2-example",
            description="Basic example of AP2 usage",
            stars=25,
            forks=8,
            issues=3,
            last_updated="2023-12-15T14:20:00Z",
            has_readme=True,
            has_license=False,
            has_ci=False,
            ap2_implementation_quality=3,
            documentation_quality=3,
            activity_score=2,
            final_rating=3,
            rating_date=datetime.now().isoformat(),
            notes="Basic AP2 implementation; Adequate documentation; Low activity"
        )
    ]
    
    # Save mock results
    try:
        os.makedirs("data", exist_ok=True)
        
        # Save detailed results
        from dataclasses import asdict
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        detailed_file = f"data/ap2_monitoring_demo_{timestamp}.json"
        with open(detailed_file, 'w') as f:
            json.dump([asdict(rating) for rating in mock_ratings], f, indent=2)
            
        # Save summary
        summary = {
            "monitoring_date": datetime.now().isoformat(),
            "total_repositories": len(mock_ratings),
            "rating_distribution": {
                "5_stars": len([r for r in mock_ratings if r.final_rating == 5]),
                "4_stars": len([r for r in mock_ratings if r.final_rating == 4]),
                "3_stars": len([r for r in mock_ratings if r.final_rating == 3]),
                "2_stars": len([r for r in mock_ratings if r.final_rating == 2]),
                "1_star": len([r for r in mock_ratings if r.final_rating == 1])
            },
            "top_rated": [
                {"name": r.full_name, "rating": r.final_rating, "url": r.url}
                for r in sorted(mock_ratings, key=lambda x: x.final_rating, reverse=True)
            ]
        }
        
        summary_file = f"data/summary_demo_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
            
        print(f"  ✅ Mock results generated:")
        print(f"    - Detailed: {detailed_file}")
        print(f"    - Summary: {summary_file}")
        print(f"    - Analyzed {len(mock_ratings)} repositories")
        
        for rating in mock_ratings:
            print(f"    - {rating.full_name}: {rating.final_rating}/5 stars")
            
    except Exception as e:
        print(f"  ❌ Mock results generation: FAIL - {e}")
        
    print()


def main():
    """Run all tests."""
    print("🔍 AP2 Monitor Test Suite")
    print("=" * 50)
    
    test_rating_calculation()
    test_data_structures()
    test_file_operations()
    generate_mock_results()
    
    print("✅ Test suite completed!")
    print("\nTo run the actual monitoring (requires GITHUB_TOKEN):")
    print("  export GITHUB_TOKEN='your_token'")
    print("  python monitor.py")


if __name__ == "__main__":
    main()