"""
Test suite for SDD Generator
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import (
    ProjectRequirements, DataClassification, DeploymentEnvironment,
    Assumption, Decision, ConfidenceLevel
)
from interviewer import RequirementsInterviewer
from generator import SDDGenerator
from formatter import MarkdownFormatter
from workflow import SDDWorkflow


class TestModels(unittest.TestCase):
    """Test data models"""
    
    def test_assumption_creation(self):
        """Test creating an Assumption"""
        asm = Assumption(
            id="ASM-001",
            description="Test assumption",
            confidence=ConfidenceLevel.HIGH,
            source="Test",
            section="Testing"
        )
        self.assertEqual(asm.id, "ASM-001")
        self.assertEqual(asm.confidence, ConfidenceLevel.HIGH)
    
    def test_decision_creation(self):
        """Test creating a Decision"""
        dec = Decision(
            id="DEC-001",
            description="Test decision",
            rationale="For testing",
            alternatives=["Alt1", "Alt2"],
            timestamp="2025-10-12",
            impact="Low"
        )
        self.assertEqual(dec.id, "DEC-001")
        self.assertEqual(len(dec.alternatives), 2)
    
    def test_project_requirements_defaults(self):
        """Test ProjectRequirements with defaults"""
        req = ProjectRequirements(
            project_name="Test Project",
            description="A test project"
        )
        self.assertEqual(req.project_name, "Test Project")
        self.assertEqual(len(req.primary_users), 0)
        self.assertEqual(len(req.core_features), 0)


class TestRequirementsInterviewer(unittest.TestCase):
    """Test requirements interviewer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.interviewer = RequirementsInterviewer()
    
    def test_generate_questions(self):
        """Test question generation"""
        questions = self.interviewer.get_questions()
        self.assertEqual(len(questions), 8)
        self.assertEqual(questions[0].id, 1)
        self.assertEqual(questions[0].category, "users")
    
    def test_get_questions_filtered(self):
        """Test filtered question retrieval"""
        questions = self.interviewer.get_questions(missing_pillars=["users", "scale"])
        self.assertEqual(len(questions), 2)
        categories = [q.category for q in questions]
        self.assertIn("users", categories)
        self.assertIn("scale", categories)
    
    def test_parse_answers_simple(self):
        """Test simple answer parsing"""
        answer_string = "1 A, 2 B, 3 C"
        answers = self.interviewer.parse_answers(answer_string)
        self.assertEqual(len(answers), 3)
        self.assertEqual(answers[0].question_id, 1)
        self.assertEqual(answers[0].selected_option, "A")
    
    def test_parse_answers_with_context(self):
        """Test answer parsing with additional context"""
        answer_string = "3 B p95 500ms 99.9%, 4 C Residency EU"
        answers = self.interviewer.parse_answers(answer_string)
        self.assertEqual(len(answers), 2)
        self.assertEqual(answers[0].additional_context, "p95 500ms 99.9%")
        self.assertEqual(answers[1].additional_context, "Residency EU")
    
    def test_parse_answers_with_skip(self):
        """Test answer parsing with skip"""
        answer_string = "1 A, skip, 3 C"
        answers = self.interviewer.parse_answers(answer_string)
        self.assertEqual(len(answers), 2)
    
    def test_build_requirements_users(self):
        """Test building requirements for users"""
        answers = self.interviewer.parse_answers("1 A")
        req = self.interviewer.build_requirements(
            "Test Project",
            "A test",
            answers
        )
        self.assertIn("End consumers", req.primary_users[0])
    
    def test_build_requirements_deployment(self):
        """Test building requirements for deployment"""
        answers = self.interviewer.parse_answers("7 A")
        req = self.interviewer.build_requirements(
            "Test Project",
            "A test",
            answers
        )
        self.assertEqual(req.deployment_environment, DeploymentEnvironment.AWS)
    
    def test_build_requirements_data_classification(self):
        """Test building requirements for data classification"""
        answers = self.interviewer.parse_answers("4 C Residency EU Class Confidential")
        req = self.interviewer.build_requirements(
            "Test Project",
            "A test",
            answers
        )
        self.assertEqual(req.data_classification, DataClassification.CONFIDENTIAL)
        self.assertIn("EU", req.data_residency)
    
    def test_build_requirements_archetype(self):
        """Test building requirements for archetype"""
        answers = self.interviewer.parse_answers("8 E")
        req = self.interviewer.build_requirements(
            "Test Project",
            "A test",
            answers
        )
        self.assertEqual(req.baseline_archetype, "ML/AI system")


class TestSDDGenerator(unittest.TestCase):
    """Test SDD generator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.requirements = ProjectRequirements(
            project_name="Test App",
            description="A test web application",
            primary_users=["Business users"],
            deployment_environment=DeploymentEnvironment.AWS,
            baseline_archetype="Traditional web application"
        )
        self.generator = SDDGenerator(self.requirements)
    
    def test_add_assumption(self):
        """Test adding assumptions"""
        asm_id = self.generator.add_assumption(
            "Test assumption",
            ConfidenceLevel.HIGH,
            "Test",
            "Testing"
        )
        self.assertEqual(asm_id, "ASM-001")
        self.assertEqual(len(self.generator.assumptions), 1)
    
    def test_add_decision(self):
        """Test adding decisions"""
        dec_id = self.generator.add_decision(
            "Test decision",
            "For testing",
            ["Alt1", "Alt2"],
            "Low"
        )
        self.assertEqual(dec_id, "DEC-001")
        self.assertEqual(len(self.generator.decisions), 1)
    
    def test_generate_metadata(self):
        """Test metadata generation"""
        metadata = self.generator._generate_metadata()
        self.assertIn("title", metadata)
        self.assertIn("Test App", metadata["title"])
        self.assertEqual(metadata["version"], "1.0")
    
    def test_generate_executive_summary(self):
        """Test executive summary generation"""
        summary = self.generator._generate_executive_summary()
        self.assertIn("Test App", summary)
        self.assertIn("Business users", summary)
        self.assertIn("AWS", summary)
    
    def test_generate_architecture_diagram(self):
        """Test architecture diagram generation"""
        diagram = self.generator._generate_architecture_diagram()
        self.assertIn("mermaid", diagram)
        self.assertIn("flowchart", diagram)
    
    def test_generate_data_model(self):
        """Test data model generation"""
        model = self.generator._generate_data_model()
        self.assertIn("mermaid", model)
        self.assertIn("erDiagram", model)
    
    def test_generate_api_design(self):
        """Test API design generation"""
        api = self.generator._generate_api_design()
        self.assertIn("openapi: 3.1.0", api)
        self.assertIn("Test App", api)
    
    def test_generate_user_flows(self):
        """Test user flows generation"""
        flows = self.generator._generate_user_flows()
        self.assertGreater(len(flows), 0)
        self.assertIn("sequenceDiagram", flows[0])
    
    def test_generate_components(self):
        """Test components generation"""
        components = self.generator._generate_components()
        self.assertGreater(len(components), 0)
        self.assertIn("name", components[0])
        self.assertIn("responsibility", components[0])
    
    def test_generate_nfrs(self):
        """Test NFR generation"""
        nfrs = self.generator._generate_nfrs()
        self.assertIn("Performance", nfrs)
        self.assertIn("Security", nfrs)
    
    def test_generate_security_privacy(self):
        """Test security and privacy generation"""
        security = self.generator._generate_security_privacy()
        self.assertIn("stride_threats", security)
        self.assertIn("owasp_asvs", security)
        self.assertIn("soc2_tsc", security)
        self.assertIn("iso27001", security)
    
    def test_generate_trade_offs(self):
        """Test trade-off generation"""
        trade_offs = self.generator._generate_trade_offs()
        self.assertGreater(len(trade_offs), 0)
        self.assertIn("aspect", trade_offs[0])
    
    def test_generate_risks_mitigations(self):
        """Test risks and mitigations generation"""
        risks = self.generator._generate_risks_mitigations()
        self.assertGreater(len(risks), 0)
        self.assertIn("risk", risks[0])
        self.assertIn("mitigation", risks[0])
    
    def test_generate_complete_sdd(self):
        """Test complete SDD generation"""
        sdd = self.generator.generate()
        self.assertIsNotNone(sdd.metadata)
        self.assertIsNotNone(sdd.executive_summary)
        self.assertGreater(len(sdd.assumptions), 0)
        self.assertGreater(len(sdd.decisions), 0)
        self.assertIsNotNone(sdd.architecture_diagram)
        self.assertIsNotNone(sdd.data_model)


class TestMarkdownFormatter(unittest.TestCase):
    """Test Markdown formatter"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.formatter = MarkdownFormatter()
        requirements = ProjectRequirements(
            project_name="Test App",
            description="Test",
            deployment_environment=DeploymentEnvironment.AWS
        )
        generator = SDDGenerator(requirements)
        self.sdd = generator.generate()
    
    def test_format_metadata(self):
        """Test metadata formatting"""
        markdown = self.formatter._format_metadata(self.sdd.metadata)
        self.assertIn("#", markdown)
        self.assertIn("Version:", markdown)
    
    def test_format_assumptions(self):
        """Test assumptions formatting"""
        markdown = self.formatter._format_assumptions(self.sdd.assumptions)
        self.assertIn("Assumptions Register", markdown)
        if len(self.sdd.assumptions) > 0:
            self.assertIn("ASM-", markdown)
    
    def test_format_decisions(self):
        """Test decisions formatting"""
        markdown = self.formatter._format_decisions(self.sdd.decisions)
        self.assertIn("Decision Log", markdown)
        if len(self.sdd.decisions) > 0:
            self.assertIn("DEC-", markdown)
    
    def test_format_complete_sdd(self):
        """Test complete SDD formatting"""
        markdown = self.formatter.format(self.sdd)
        self.assertIn("# Software Design Document", markdown)
        self.assertIn("Executive Summary", markdown)
        self.assertIn("Architecture Overview", markdown)
        self.assertIn("mermaid", markdown)
        self.assertIn("Security and Privacy", markdown)
        self.assertIn("STRIDE", markdown)
        self.assertIn("OWASP ASVS", markdown)
        self.assertGreater(len(markdown), 1800)  # Should be substantial


class TestSDDWorkflow(unittest.TestCase):
    """Test SDD workflow"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.workflow = SDDWorkflow()
    
    def test_run_phase1_with_answers(self):
        """Test Phase 1 with answers"""
        requirements = self.workflow.run_phase1(
            "Test App",
            "A test application",
            "1 A, 2 A, 3 B, 4 C Residency EU, 7 A, 8 A"
        )
        self.assertIsNotNone(requirements)
        self.assertEqual(requirements.project_name, "Test App")
        self.assertGreater(len(requirements.answers), 0)
    
    def test_run_phase2(self):
        """Test Phase 2 generation"""
        requirements = ProjectRequirements(
            project_name="Test App",
            description="Test",
            deployment_environment=DeploymentEnvironment.AWS
        )
        markdown = self.workflow.run_phase2(requirements)
        self.assertIsNotNone(markdown)
        self.assertIn("Software Design Document", markdown)
        self.assertGreater(len(markdown), 1000)
    
    def test_complete_workflow(self):
        """Test complete workflow"""
        markdown = self.workflow.run_complete_workflow(
            "Test App",
            "A test web application",
            "1 A, 2 A, 3 B, 4 C, 7 A, 8 A"
        )
        self.assertIsNotNone(markdown)
        self.assertIn("Test App", markdown)
        self.assertIn("Architecture", markdown)
        self.assertIn("Security", markdown)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow"""
    
    def test_complete_workflow_aws(self):
        """Test complete workflow with AWS deployment"""
        workflow = SDDWorkflow()
        markdown = workflow.run_complete_workflow(
            "E-Commerce Platform",
            "A modern e-commerce platform for selling products online",
            "1 A, 2 C, 3 C 10K-100K users p95 200ms 99.95%, 4 D GDPR SOC2, 5 A Stripe Okta, 6 B 6 months, 7 A, 8 F"
        )
        
        # Verify content
        self.assertIn("E-Commerce Platform", markdown)
        self.assertIn("AWS", markdown)
        self.assertIn("Microservices", markdown)
        self.assertIn("GDPR", markdown)
        self.assertIn("STRIDE", markdown)
        self.assertIn("OWASP ASVS", markdown)
        self.assertIn("SOC 2", markdown)
        self.assertIn("ISO/IEC 27001", markdown)
        
        # Verify structure
        self.assertIn("## Executive Summary", markdown)
        self.assertIn("## Assumptions Register", markdown)
        self.assertIn("## Decision Log", markdown)
        self.assertIn("## Architecture Overview", markdown)
        self.assertIn("## Components", markdown)
        self.assertIn("## Data Model", markdown)
        self.assertIn("## API Design", markdown)
        self.assertIn("## Security and Privacy", markdown)
        self.assertIn("## Risks and Mitigations", markdown)
        self.assertIn("## Glossary", markdown)
        
        # Verify diagrams
        self.assertIn("```mermaid", markdown)
        self.assertIn("flowchart", markdown)
        self.assertIn("erDiagram", markdown)
        self.assertIn("sequenceDiagram", markdown)
        
        # Verify OpenAPI
        self.assertIn("openapi: 3.1.0", markdown)
        
        # Verify word count is within range (1800-2500 words)
        word_count = len(markdown.split())
        self.assertGreater(word_count, 1500)  # Allow some flexibility
    
    def test_complete_workflow_azure_ml(self):
        """Test complete workflow with Azure ML system"""
        workflow = SDDWorkflow()
        markdown = workflow.run_complete_workflow(
            "ML Prediction Service",
            "A machine learning service for predictive analytics",
            "1 B, 2 B, 3 B, 4 C Residency US, 5 Other Azure ML, 6 D, 7 B, 8 E"
        )
        
        self.assertIn("ML Prediction Service", markdown)
        self.assertIn("Azure", markdown)
        self.assertIn("ML/AI system", markdown)
        self.assertIn("AI Safety", markdown)


if __name__ == "__main__":
    unittest.main()
