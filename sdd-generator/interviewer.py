"""
Phase 1: Requirements Interview Module
Handles question generation and answer processing
"""

from typing import List, Dict, Optional
try:
    from .models import Question, Answer, ProjectRequirements, DataClassification, DeploymentEnvironment
except ImportError:
    from models import Question, Answer, ProjectRequirements, DataClassification, DeploymentEnvironment


class RequirementsInterviewer:
    """Manages the requirements gathering interview process"""
    
    def __init__(self):
        self.questions = self._generate_questions()
    
    def _generate_questions(self) -> List[Question]:
        """Generate the standard set of interview questions"""
        questions = [
            Question(
                id=1,
                text="Who are the primary users and personas for this application?",
                options=[
                    "A) End consumers (B2C)",
                    "B) Business users (B2B)",
                    "C) Internal employees",
                    "D) Mixed user base"
                ],
                category="users"
            ),
            Question(
                id=2,
                text="What are the core features and scope?",
                options=[
                    "A) User authentication and profiles",
                    "B) Data processing and analytics",
                    "C) E-commerce/transactions",
                    "D) Content management",
                    "E) Real-time collaboration",
                    "F) Other (specify)"
                ],
                category="features"
            ),
            Question(
                id=3,
                text="What are the scale and SLO requirements?",
                options=[
                    "A) < 1000 users, latency < 1s, 99% availability",
                    "B) 1K-10K users, p95 500ms, 99.9% availability",
                    "C) 10K-100K users, p95 200ms, 99.95% availability",
                    "D) > 100K users, p95 < 100ms, 99.99% availability"
                ],
                category="scale"
            ),
            Question(
                id=4,
                text="What is the data sensitivity, classification, residency, and compliance?",
                options=[
                    "A) Public data, no special requirements",
                    "B) Internal data, basic security",
                    "C) Confidential data with specific residency (specify region)",
                    "D) Highly regulated (GDPR, HIPAA, SOC 2, ISO 27001)"
                ],
                category="data"
            ),
            Question(
                id=5,
                text="What external integrations are required?",
                options=[
                    "A) Identity Provider (e.g., Okta, Auth0)",
                    "B) Payment processing (e.g., Stripe, PayPal)",
                    "C) Analytics (e.g., Segment, Mixpanel)",
                    "D) Email services (e.g., SendGrid, SES)",
                    "E) Other (specify)"
                ],
                category="integrations"
            ),
            Question(
                id=6,
                text="What are the key constraints?",
                options=[
                    "A) Budget constraints (specify)",
                    "B) Timeline constraints (specify)",
                    "C) Team skill constraints (specify)",
                    "D) No major constraints"
                ],
                category="constraints"
            ),
            Question(
                id=7,
                text="What is the preferred deployment environment?",
                options=[
                    "A) AWS",
                    "B) Azure",
                    "C) Google Cloud Platform",
                    "D) On-Premise",
                    "E) Hybrid"
                ],
                category="deployment"
            ),
            Question(
                id=8,
                text="What is the baseline architecture archetype?",
                options=[
                    "A) Traditional web application",
                    "B) Event-driven architecture",
                    "C) Batch/ETL system",
                    "D) Mobile backend",
                    "E) ML/AI system",
                    "F) Microservices"
                ],
                category="archetype"
            )
        ]
        return questions
    
    def get_questions(self, missing_pillars: Optional[List[str]] = None) -> List[Question]:
        """
        Get questions for the interview
        
        Args:
            missing_pillars: List of specific categories to ask about, or None for all
        
        Returns:
            List of questions to ask
        """
        if missing_pillars is None:
            return self.questions
        
        return [q for q in self.questions if q.category in missing_pillars]
    
    def parse_answers(self, answer_string: str) -> List[Answer]:
        """
        Parse compact answer format like "1 C, 2 A, 3 B p95 500ms 99.9%, 4 B Residency EU Class Confidential"
        
        Args:
            answer_string: Compact answer string from user
        
        Returns:
            List of Answer objects
        """
        answers = []
        parts = answer_string.split(',')
        
        for part in parts:
            part = part.strip()
            if part.lower() == 'skip':
                continue
            
            # Extract question number and answer
            tokens = part.split()
            if len(tokens) < 2:
                continue
            
            try:
                question_id = int(tokens[0])
                selected_option = tokens[1]
                additional_context = ' '.join(tokens[2:]) if len(tokens) > 2 else None
                
                answers.append(Answer(
                    question_id=question_id,
                    selected_option=selected_option,
                    additional_context=additional_context
                ))
            except (ValueError, IndexError):
                continue
        
        return answers
    
    def build_requirements(
        self,
        project_name: str,
        description: str,
        answers: List[Answer]
    ) -> ProjectRequirements:
        """
        Build ProjectRequirements from answers
        
        Args:
            project_name: Name of the project
            description: Basic project description
            answers: List of answers from the interview
        
        Returns:
            ProjectRequirements object
        """
        requirements = ProjectRequirements(
            project_name=project_name,
            description=description,
            answers=answers
        )
        
        # Process answers to fill in requirements
        answer_dict = {a.question_id: a for a in answers}
        
        # Question 1: Users
        if 1 in answer_dict:
            option = answer_dict[1].selected_option
            if option == 'A':
                requirements.primary_users = ["End consumers (B2C)"]
            elif option == 'B':
                requirements.primary_users = ["Business users (B2B)"]
            elif option == 'C':
                requirements.primary_users = ["Internal employees"]
            elif option == 'D':
                requirements.primary_users = ["Mixed user base"]
        
        # Question 2: Features
        if 2 in answer_dict:
            context = answer_dict[2].additional_context or ""
            requirements.core_features = [
                f"Feature: {answer_dict[2].selected_option} {context}"
            ]
        
        # Question 3: Scale
        if 3 in answer_dict:
            requirements.scale_requirements = {
                "level": answer_dict[3].selected_option,
                "details": answer_dict[3].additional_context or ""
            }
        
        # Question 4: Data
        if 4 in answer_dict:
            option = answer_dict[4].selected_option
            context = answer_dict[4].additional_context or ""
            
            if 'Confidential' in context:
                requirements.data_classification = DataClassification.CONFIDENTIAL
            elif option == 'D':
                requirements.data_classification = DataClassification.RESTRICTED
            elif option == 'B':
                requirements.data_classification = DataClassification.INTERNAL
            else:
                requirements.data_classification = DataClassification.PUBLIC
            
            if 'EU' in context or 'US' in context or 'Asia' in context:
                requirements.data_residency = context
            
            if option == 'D':
                requirements.compliance_requirements = ["GDPR", "SOC 2", "ISO 27001"]
        
        # Question 5: Integrations
        if 5 in answer_dict:
            context = answer_dict[5].additional_context or ""
            requirements.external_integrations = [context] if context else []
        
        # Question 6: Constraints
        if 6 in answer_dict:
            option = answer_dict[6].selected_option
            context = answer_dict[6].additional_context or ""
            requirements.constraints = {
                "type": option,
                "details": context
            }
        
        # Question 7: Deployment
        if 7 in answer_dict:
            option = answer_dict[7].selected_option
            env_map = {
                'A': DeploymentEnvironment.AWS,
                'B': DeploymentEnvironment.AZURE,
                'C': DeploymentEnvironment.GCP,
                'D': DeploymentEnvironment.ON_PREMISE,
                'E': DeploymentEnvironment.HYBRID
            }
            requirements.deployment_environment = env_map.get(option)
        
        # Question 8: Archetype
        if 8 in answer_dict:
            option = answer_dict[8].selected_option
            archetype_map = {
                'A': "Traditional web application",
                'B': "Event-driven architecture",
                'C': "Batch/ETL system",
                'D': "Mobile backend",
                'E': "ML/AI system",
                'F': "Microservices"
            }
            requirements.baseline_archetype = archetype_map.get(option)
        
        return requirements
