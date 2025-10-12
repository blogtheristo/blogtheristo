#!/usr/bin/env python3
"""
Command-line interface for SDD Generator
"""

import argparse
import sys
try:
    from .workflow import SDDWorkflow
except ImportError:
    from workflow import SDDWorkflow


def main():
    parser = argparse.ArgumentParser(
        description="Grok 4 Heavy - Software Design Document Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show interview questions
  python -m sdd-generator.cli --name "MyApp" --description "A web application"
  
  # Generate SDD with answers
  python -m sdd-generator.cli --name "MyApp" --description "A web app" \\
    --answers "1 A, 2 A, 3 B p95 500ms 99.9%, 4 C Residency EU, 5 A, 6 D, 7 A, 8 A" \\
    --output sdd.md
        """
    )
    
    parser.add_argument(
        "--name",
        required=True,
        help="Project name"
    )
    
    parser.add_argument(
        "--description",
        required=True,
        help="Basic project description"
    )
    
    parser.add_argument(
        "--answers",
        help="Compact answer string (e.g., '1 C, 2 A, 3 B, ...')"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path for the SDD (Markdown format)"
    )
    
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()
    
    workflow = SDDWorkflow()
    
    try:
        if args.interactive:
            # Interactive mode
            print("\n=== SDD Generator - Interactive Mode ===\n")
            print(f"Project: {args.name}")
            print(f"Description: {args.description}\n")
            
            # Show questions
            workflow.run_phase1(args.name, args.description, None)
            
            # Get answers from user
            print("Enter your answers:")
            answer_string = input("> ").strip()
            
            # Generate SDD
            markdown = workflow.run_complete_workflow(
                args.name,
                args.description,
                answer_string,
                args.output
            )
            
            if not args.output:
                print("\n" + "="*80)
                print(markdown)
        
        elif args.answers:
            # Non-interactive mode with answers provided
            markdown = workflow.run_complete_workflow(
                args.name,
                args.description,
                args.answers,
                args.output
            )
            
            if not args.output:
                print("\n" + "="*80)
                print(markdown)
        
        else:
            # Show questions only
            workflow.run_phase1(args.name, args.description, None)
            print("\nUse --answers to provide responses, or --interactive for guided mode.")
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
