"""
Main workflow orchestrator for SDD generation
"""

from typing import Optional
try:
    from .interviewer import RequirementsInterviewer
    from .generator import SDDGenerator
    from .formatter import MarkdownFormatter
    from .models import ProjectRequirements
except ImportError:
    from interviewer import RequirementsInterviewer
    from generator import SDDGenerator
    from formatter import MarkdownFormatter
    from models import ProjectRequirements


class SDDWorkflow:
    """Orchestrates the complete SDD generation workflow"""
    
    def __init__(self):
        self.interviewer = RequirementsInterviewer()
        self.formatter = MarkdownFormatter()
    
    def run_phase1(
        self,
        project_name: str,
        description: str,
        answer_string: Optional[str] = None
    ) -> ProjectRequirements:
        """
        Run Phase 1: Requirements Interview
        
        Args:
            project_name: Name of the project
            description: Basic project description
            answer_string: Compact answer string, or None to return questions
        
        Returns:
            ProjectRequirements object
        """
        if answer_string is None:
            # Return questions for the user to answer
            questions = self.interviewer.get_questions()
            print("\n=== Phase 1: Requirements Interview ===\n")
            for q in questions:
                print(f"{q.id}. {q.text}")
                for option in q.options:
                    print(f"   {option}")
                print()
            print("Please answer in format: '1 C, 2 A, 3 B p95 500ms 99.9%, ...'")
            print("You can also reply 'skip' for any question.\n")
            return None
        
        # Parse answers and build requirements
        answers = self.interviewer.parse_answers(answer_string)
        requirements = self.interviewer.build_requirements(
            project_name=project_name,
            description=description,
            answers=answers
        )
        
        return requirements
    
    def run_phase2(self, requirements: ProjectRequirements) -> str:
        """
        Run Phase 2: SDD Draft Generation
        
        Args:
            requirements: ProjectRequirements from Phase 1
        
        Returns:
            Markdown formatted SDD
        """
        print("\n=== Phase 2: SDD Draft Generation ===\n")
        print("Generating Software Design Document...\n")
        
        # Generate SDD
        generator = SDDGenerator(requirements)
        sdd = generator.generate()
        
        # Format as Markdown
        markdown = self.formatter.format(sdd)
        
        print("SDD generation complete!")
        print(f"Document contains {len(sdd.assumptions)} assumptions and {len(sdd.decisions)} decisions")
        print(f"Approximate word count: {len(markdown.split())} words\n")
        
        return markdown
    
    def run_complete_workflow(
        self,
        project_name: str,
        description: str,
        answer_string: str,
        output_file: Optional[str] = None
    ) -> str:
        """
        Run complete workflow (Phase 1 + Phase 2)
        
        Args:
            project_name: Name of the project
            description: Basic project description
            answer_string: Compact answer string
            output_file: Optional file path to save the SDD
        
        Returns:
            Markdown formatted SDD
        """
        # Phase 1
        requirements = self.run_phase1(project_name, description, answer_string)
        
        # Phase 2
        markdown = self.run_phase2(requirements)
        
        # Save to file if requested
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"SDD saved to {output_file}")
        
        return markdown
