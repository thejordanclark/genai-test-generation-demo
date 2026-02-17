# GenAI Bootcamp - Test Suite Generation Demo

This repository demonstrates AI-assisted test generation for GxP-validated systems.

## Purpose
- Generate comprehensive test suites using GitHub Copilot
- Capture validation evidence
- Demonstrate CSV/CSA-compliant testing practices

## Modules Under Test
1. **Patient Validator** - Validates patient demographic data
2. **Adverse Event Processor** - Processes and categorizes AE data
3. **Protocol Parser** - Parses clinical trial protocol documents

## Testing Strategy
- Unit tests for individual functions
- Integration tests for workflows
- Property-based tests for data validation
- Boundary tests for edge cases

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Run with detailed HTML report
pytest --html=reports/test_report.html --self-contained-html

# Run specific test file
pytest tests/test_patient_validator.py -v
