#!/usr/bin/env python3
"""
Demo script showing SDD Generator usage
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from workflow import SDDWorkflow

def demo_show_questions():
    """Demo: Show the interview questions"""
    print("=" * 80)
    print("DEMO 1: Show Interview Questions")
    print("=" * 80)
    print()
    
    workflow = SDDWorkflow()
    workflow.run_phase1(
        project_name="Demo App",
        description="A demo application",
        answer_string=None
    )
    print()

def demo_generate_sdd():
    """Demo: Generate a complete SDD"""
    print("=" * 80)
    print("DEMO 2: Generate Complete SDD")
    print("=" * 80)
    print()
    
    workflow = SDDWorkflow()
    
    # Example project
    project_name = "Smart Home Platform"
    description = "An IoT platform for managing smart home devices with real-time monitoring"
    answers = "1 A, 2 E Real-time data, 3 B 1K-10K users p95 500ms 99.9%, 4 C Residency US, 5 Other AWS IoT MQTT, 6 B 9 months, 7 A, 8 B"
    
    print(f"Project: {project_name}")
    print(f"Description: {description}")
    print(f"Answers: {answers}")
    print()
    
    # Generate SDD
    markdown = workflow.run_complete_workflow(
        project_name=project_name,
        description=description,
        answer_string=answers,
        output_file=None
    )
    
    print()
    print("=" * 80)
    print("GENERATED SDD PREVIEW (first 500 characters):")
    print("=" * 80)
    print(markdown[:500])
    print("\n... (truncated) ...\n")
    print(f"Total length: {len(markdown)} characters, {len(markdown.split())} words")
    print()

def demo_custom_requirements():
    """Demo: Build requirements programmatically"""
    print("=" * 80)
    print("DEMO 3: Programmatic SDD Generation")
    print("=" * 80)
    print()
    
    from models import ProjectRequirements, DeploymentEnvironment
    from generator import SDDGenerator
    from formatter import MarkdownFormatter
    
    # Create requirements directly
    requirements = ProjectRequirements(
        project_name="API Gateway Service",
        description="High-performance API gateway for microservices",
        primary_users=["Internal services", "External partners"],
        core_features=["Rate limiting", "Authentication", "Request routing"],
        deployment_environment=DeploymentEnvironment.AWS,
        baseline_archetype="Microservices"
    )
    
    # Generate SDD
    generator = SDDGenerator(requirements)
    sdd = generator.generate()
    
    # Format as Markdown
    formatter = MarkdownFormatter()
    markdown = formatter.format(sdd)
    
    print(f"Generated SDD for: {requirements.project_name}")
    print(f"Assumptions: {len(sdd.assumptions)}")
    print(f"Decisions: {len(sdd.decisions)}")
    print(f"Components: {len(sdd.components)}")
    print(f"Word count: {len(markdown.split())}")
    print()

def main():
    """Run all demos"""
    print("\n" + "=" * 80)
    print("SDD GENERATOR - DEMONSTRATION")
    print("=" * 80)
    print()
    
    try:
        demo_show_questions()
        print("\n" + "=" * 40)
        print("Moving to Demo 2...")
        print("=" * 40 + "\n")
        
        demo_generate_sdd()
        print("\n" + "=" * 40)
        print("Moving to Demo 3...")
        print("=" * 40 + "\n")
        
        demo_custom_requirements()
        
        print("=" * 80)
        print("DEMOS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print("To use the SDD Generator:")
        print("  python3 cli.py --name 'MyApp' --description 'My app description' --interactive")
        print()
        
    except KeyboardInterrupt:
        print("\n\nDemo cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
