# SDD Generator Quick Reference

## Quick Start

Generate an SDD in 3 steps:

```bash
cd sdd-generator

# Step 1: See the questions
python3 cli.py --name "MyApp" --description "My application"

# Step 2: Prepare your answers
# Format: "1 A, 2 B, 3 C details, 4 D, ..."

# Step 3: Generate SDD
python3 cli.py --name "MyApp" --description "My application" \
  --answers "1 A, 2 B, 3 C, 4 D, 5 A, 6 D, 7 A, 8 F" \
  --output my-sdd.md
```

## Answer Format Cheat Sheet

Format: `QuestionNumber OptionLetter [additional context], ...`

Examples:
- Simple: `"1 A, 2 B, 3 C"`
- With context: `"3 B p95 500ms 99.9%, 4 C Residency EU"`
- With details: `"5 Other Stripe Okta SendGrid, 6 B Timeline 6 months"`
- Skip: `"1 A, skip, 3 C"` (uses defaults for question 2)

## The 8 Questions

1. **Users**: A) B2C, B) B2B, C) Internal, D) Mixed
2. **Features**: A) Auth, B) Analytics, C) E-commerce, D) CMS, E) Collaboration, F) Other
3. **Scale**: A) <1K users, B) 1K-10K, C) 10K-100K, D) >100K
4. **Data**: A) Public, B) Internal, C) Confidential+region, D) Highly regulated
5. **Integrations**: A) IdP, B) Payments, C) Analytics, D) Email, E) Other
6. **Constraints**: A) Budget, B) Timeline, C) Team skills, D) None
7. **Deployment**: A) AWS, B) Azure, C) GCP, D) On-Premise, E) Hybrid
8. **Archetype**: A) Web app, B) Event-driven, C) Batch/ETL, D) Mobile backend, E) ML/AI, F) Microservices

## Common Use Cases

### E-Commerce Platform
```bash
python3 cli.py --name "E-Commerce Platform" \
  --description "Online shopping with payments and inventory" \
  --answers "1 A, 2 C, 3 C 10K-100K p95 200ms, 4 D GDPR SOC2, 5 Other Stripe, 6 B 6mo, 7 A, 8 F" \
  --output ecommerce-sdd.md
```

### ML/AI Service
```bash
python3 cli.py --name "ML Prediction Service" \
  --description "Machine learning predictions via API" \
  --answers "1 B, 2 B, 3 B, 4 C Residency US, 5 Other Azure ML, 6 D, 7 B, 8 E" \
  --output ml-service-sdd.md
```

### Mobile Backend
```bash
python3 cli.py --name "Mobile App Backend" \
  --description "REST API for iOS/Android mobile app" \
  --answers "1 A, 2 A, 3 B, 4 B, 5 A Auth0, 6 B 3mo, 7 A, 8 D" \
  --output mobile-backend-sdd.md
```

### IoT Platform
```bash
python3 cli.py --name "Smart Home Platform" \
  --description "IoT platform for smart home devices" \
  --answers "1 A, 2 E Real-time monitoring, 3 B, 4 C, 5 Other AWS IoT, 6 D, 7 A, 8 B" \
  --output iot-platform-sdd.md
```

## Python API

```python
from workflow import SDDWorkflow

workflow = SDDWorkflow()

# Generate SDD
markdown = workflow.run_complete_workflow(
    project_name="My App",
    description="My app description",
    answer_string="1 A, 2 B, 3 C, 4 D, 5 A, 6 D, 7 A, 8 F",
    output_file="my-sdd.md"  # Optional
)

print(markdown)
```

## Output Sections

Every generated SDD includes:

✅ Document Metadata (version, date, author, status)
✅ Executive Summary
✅ Assumptions Register (with confidence levels)
✅ Decision Log (with rationale and alternatives)
✅ Trade-off Table
✅ Architecture Overview + Mermaid Diagram
✅ Components
✅ Data Model (Mermaid ER Diagram)
✅ API Design (OpenAPI 3.1 YAML)
✅ User Flows (Mermaid Sequence Diagrams)
✅ Non-Functional Requirements
✅ Security & Privacy (STRIDE, OWASP ASVS, SOC 2, ISO 27001)
✅ Observability
✅ Testing and Quality
✅ Deployment and Operations
✅ Technology Choices (with Provider Selection Matrix)
✅ Risks and Mitigations
✅ Accessibility and Internationalization
✅ Open Questions
✅ Glossary

## Testing

```bash
# Run all tests
python3 test_sdd_generator.py

# Run with verbose output
python3 test_sdd_generator.py -v

# Run specific test
python3 test_sdd_generator.py TestSDDWorkflow.test_complete_workflow
```

## Demo

```bash
# Run interactive demo
python3 demo.py
```

## Tips

1. **Be specific**: Add context like "p95 500ms 99.9%" for scale requirements
2. **Use skip**: Skip questions you're unsure about - defaults will be used
3. **Combine options**: "5 Other Stripe Okta SendGrid" for multiple integrations
4. **Review output**: Check the generated SDD and iterate on answers if needed
5. **Save examples**: Keep successful SDDs as templates for similar projects

## Customization

To customize the generator:

- **Add questions**: Edit `interviewer.py` → `_generate_questions()`
- **Modify sections**: Edit `generator.py` → `_generate_*()` methods
- **Change format**: Edit `formatter.py` → `_format_*()` methods
- **New data types**: Add to `models.py` enums

## Troubleshooting

**Issue**: "No module named 'models'"
- **Fix**: Run from the `sdd-generator/` directory

**Issue**: Generated SDD seems incomplete
- **Fix**: Provide more detailed answers with context

**Issue**: Want more/less detail in a section
- **Fix**: Customize the relevant `_generate_*()` method in `generator.py`

## Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Run the demo: `python3 demo.py`
3. Run tests to verify installation: `python3 test_sdd_generator.py`
4. Review example output: `examples/ecommerce-platform-sdd.md`

## Version

SDD Generator v0.1.0 (2025-10-12)
