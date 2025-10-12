"""
Markdown formatter for Software Design Documents
"""

from typing import List, Dict
try:
    from .models import SoftwareDesignDocument, Assumption, Decision, ConfidenceLevel
except ImportError:
    from models import SoftwareDesignDocument, Assumption, Decision, ConfidenceLevel


class MarkdownFormatter:
    """Formats SDD as clean Markdown"""
    
    def format(self, sdd: SoftwareDesignDocument) -> str:
        """Format complete SDD as Markdown"""
        sections = []
        
        # Document Metadata
        sections.append(self._format_metadata(sdd.metadata))
        
        # Executive Summary
        sections.append(sdd.executive_summary)
        
        # Assumptions Register
        sections.append(self._format_assumptions(sdd.assumptions))
        
        # Decision Log
        sections.append(self._format_decisions(sdd.decisions))
        
        # Trade-off Table
        sections.append(self._format_trade_offs(sdd.trade_offs))
        
        # Architecture Overview
        sections.append(sdd.architecture_overview)
        sections.append("\n### Architecture Diagram\n")
        sections.append(sdd.architecture_diagram)
        
        # Components
        sections.append(self._format_components(sdd.components))
        
        # Data Model
        sections.append("\n## Data Model\n")
        sections.append(sdd.data_model)
        
        # API Design
        sections.append("\n## API Design\n")
        sections.append(sdd.api_design)
        
        # User Flows
        sections.append(self._format_user_flows(sdd.user_flows))
        
        # Non-Functional Requirements
        sections.append(self._format_nfrs(sdd.non_functional_requirements))
        
        # Security and Privacy
        sections.append(self._format_security(sdd.security_privacy))
        
        # Observability
        sections.append(self._format_dict_section("Observability", sdd.observability))
        
        # Testing and Quality
        sections.append(self._format_dict_section("Testing and Quality", sdd.testing_quality))
        
        # Deployment and Operations
        sections.append(self._format_dict_section("Deployment and Operations", sdd.deployment_operations))
        
        # Technology Choices
        sections.append(self._format_technology_choices(sdd.technology_choices))
        
        # Risks and Mitigations
        sections.append(self._format_risks(sdd.risks_mitigations))
        
        # Accessibility and Internationalization
        sections.append(self._format_dict_section("Accessibility and Internationalization", sdd.accessibility_i18n))
        
        # Open Questions
        sections.append(self._format_open_questions(sdd.open_questions))
        
        # Glossary
        sections.append(self._format_glossary(sdd.glossary))
        
        return "\n\n".join(sections)
    
    def _format_metadata(self, metadata: Dict[str, str]) -> str:
        """Format document metadata"""
        lines = [f"# {metadata.get('title', 'Software Design Document')}"]
        lines.append("")
        lines.append("## Document Metadata")
        lines.append("")
        lines.append(f"- **Version:** {metadata.get('version', '1.0')}")
        lines.append(f"- **Date:** {metadata.get('date', 'N/A')}")
        lines.append(f"- **Author:** {metadata.get('author', 'N/A')}")
        lines.append(f"- **Status:** {metadata.get('status', 'Draft')}")
        return "\n".join(lines)
    
    def _format_assumptions(self, assumptions: List[Assumption]) -> str:
        """Format assumptions register"""
        if not assumptions:
            return "## Assumptions Register\n\nNo assumptions recorded."
        
        lines = ["## Assumptions Register and Confidence"]
        lines.append("")
        lines.append("| ID | Description | Confidence | Source | Section |")
        lines.append("|----|-------------|------------|--------|---------|")
        
        for asm in assumptions:
            lines.append(
                f"| {asm.id} | {asm.description} | {asm.confidence.value} | "
                f"{asm.source} | {asm.section} |"
            )
        
        lines.append("")
        lines.append("**Confidence Levels:**")
        lines.append("- **High:** Well-validated, low risk")
        lines.append("- **Medium:** Reasonable assumption, moderate risk")
        lines.append("- **Low:** Uncertain, requires validation")
        
        return "\n".join(lines)
    
    def _format_decisions(self, decisions: List[Decision]) -> str:
        """Format decision log"""
        if not decisions:
            return "## Decision Log\n\nNo decisions recorded."
        
        lines = ["## Decision Log"]
        lines.append("")
        
        for dec in decisions:
            lines.append(f"### {dec.id}: {dec.description}")
            lines.append("")
            lines.append(f"**Rationale:** {dec.rationale}")
            lines.append("")
            lines.append("**Alternatives Considered:**")
            for alt in dec.alternatives:
                lines.append(f"- {alt}")
            lines.append("")
            lines.append(f"**Impact:** {dec.impact}")
            lines.append("")
            lines.append(f"**Timestamp:** {dec.timestamp}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_trade_offs(self, trade_offs: List[Dict[str, str]]) -> str:
        """Format trade-off table"""
        if not trade_offs:
            return "## Trade-off Table\n\nNo trade-offs documented."
        
        lines = ["## Trade-off Table"]
        lines.append("")
        lines.append("| Aspect | Option A | Option B | Chosen | Rationale |")
        lines.append("|--------|----------|----------|--------|-----------|")
        
        for trade_off in trade_offs:
            lines.append(
                f"| {trade_off['aspect']} | {trade_off['option_a']} | "
                f"{trade_off['option_b']} | {trade_off['chosen']} | "
                f"{trade_off['rationale']} |"
            )
        
        return "\n".join(lines)
    
    def _format_components(self, components: List[Dict[str, str]]) -> str:
        """Format components section"""
        if not components:
            return "## Components\n\nNo components defined."
        
        lines = ["## Components"]
        lines.append("")
        
        for comp in components:
            lines.append(f"### {comp['name']}")
            lines.append("")
            lines.append(f"**Responsibility:** {comp['responsibility']}")
            lines.append("")
            lines.append(f"**Technology:** {comp['technology']}")
            lines.append("")
            lines.append(f"**Interfaces:** {comp['interfaces']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_user_flows(self, user_flows: List[str]) -> str:
        """Format user flows section"""
        if not user_flows:
            return "## User Flows\n\nNo user flows defined."
        
        lines = ["## User Flows"]
        lines.append("")
        
        for i, flow in enumerate(user_flows, 1):
            lines.append(f"### Flow {i}")
            lines.append("")
            lines.append(flow)
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_nfrs(self, nfrs: Dict[str, str]) -> str:
        """Format non-functional requirements"""
        lines = ["## Non-Functional Requirements"]
        lines.append("")
        
        for key, value in nfrs.items():
            lines.append(f"**{key}:** {value}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_security(self, security: Dict[str, str]) -> str:
        """Format security and privacy section"""
        lines = ["## Security and Privacy"]
        lines.append("")
        
        if "overview" in security:
            lines.append(security["overview"])
            lines.append("")
        
        if "stride_threats" in security:
            lines.append("### STRIDE Threat Model")
            lines.append("")
            lines.append(security["stride_threats"])
            lines.append("")
        
        if "owasp_asvs" in security:
            lines.append("### OWASP ASVS Compliance")
            lines.append("")
            lines.append(security["owasp_asvs"])
            lines.append("")
        
        if "soc2_tsc" in security:
            lines.append("### SOC 2 Trust Services Criteria")
            lines.append("")
            lines.append(security["soc2_tsc"])
            lines.append("")
        
        if "iso27001" in security:
            lines.append("### ISO/IEC 27001 Controls")
            lines.append("")
            lines.append(security["iso27001"])
            lines.append("")
        
        if "ai_safety" in security:
            lines.append("### AI Safety")
            lines.append("")
            lines.append(security["ai_safety"])
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_dict_section(self, title: str, content: Dict[str, str]) -> str:
        """Format a generic dictionary section"""
        lines = [f"## {title}"]
        lines.append("")
        
        for key, value in content.items():
            lines.append(f"**{key}:** {value}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_technology_choices(self, choices: Dict[str, str]) -> str:
        """Format technology choices section"""
        lines = ["## Technology Choices and Trade-offs"]
        lines.append("")
        
        for key, value in choices.items():
            if key == "Provider_Matrix":
                lines.append(value)
            else:
                lines.append(f"**{key}:** {value}")
                lines.append("")
        
        return "\n".join(lines)
    
    def _format_risks(self, risks: List[Dict[str, str]]) -> str:
        """Format risks and mitigations"""
        if not risks:
            return "## Risks and Mitigations\n\nNo risks identified."
        
        lines = ["## Risks and Mitigations"]
        lines.append("")
        lines.append("| Risk | Likelihood | Impact | Mitigation |")
        lines.append("|------|------------|--------|------------|")
        
        for risk in risks:
            lines.append(
                f"| {risk['risk']} | {risk['likelihood']} | "
                f"{risk['impact']} | {risk['mitigation']} |"
            )
        
        return "\n".join(lines)
    
    def _format_open_questions(self, questions: List[str]) -> str:
        """Format open questions"""
        if not questions:
            return "## Open Questions\n\nNo open questions."
        
        lines = ["## Open Questions"]
        lines.append("")
        
        for question in questions:
            lines.append(f"- {question}")
        
        return "\n".join(lines)
    
    def _format_glossary(self, glossary: Dict[str, str]) -> str:
        """Format glossary"""
        if not glossary:
            return "## Glossary\n\nNo terms defined."
        
        lines = ["## Glossary"]
        lines.append("")
        
        for term, definition in sorted(glossary.items()):
            lines.append(f"**{term}:** {definition}")
            lines.append("")
        
        return "\n".join(lines)
