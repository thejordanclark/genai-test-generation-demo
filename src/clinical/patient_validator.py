"""Patient demographic data validator for clinical trials."""

import re
from datetime import datetime
from typing import Dict, List, Tuple
import jsonschema


class PatientValidator:
    """Validates patient demographic data against clinical trial requirements."""
    
    SCHEMA = {
        "type": "object",
        "properties": {
            "patient_id": {"type": "string", "pattern": "^PAT[0-9]{6}$"},
            "age": {"type": "integer", "minimum": 18, "maximum": 85},
            "gender": {"type": "string", "enum": ["M", "F", "O"]},
            "enrollment_date": {"type": "string", "format": "date"},
            "site_id": {"type": "string", "pattern": "^SITE[0-9]{3}$"},
            "consent_signed": {"type": "boolean"}
        },
        "required": ["patient_id", "age", "gender", "enrollment_date", "site_id", "consent_signed"]
    }
    
    def __init__(self):
        """Initialize validator with schema."""
        self.validator = jsonschema.Draft7Validator(self.SCHEMA)
    
    def validate(self, patient_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate patient demographic data.
        
        Args:
            patient_data: Dictionary containing patient information
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Schema validation
        for error in self.validator.iter_errors(patient_data):
            errors.append(f"{error.json_path}: {error.message}")
        
        # Business rule validations
        if "enrollment_date" in patient_data:
            try:
                enrollment = datetime.fromisoformat(patient_data["enrollment_date"])
                if enrollment > datetime.now():
                    errors.append("enrollment_date: Cannot be in the future")
            except ValueError:
                errors.append("enrollment_date: Invalid date format")
        
        # Consent validation
        if patient_data.get("consent_signed") is False:
            errors.append("consent_signed: Patient must have signed consent")
        
        return len(errors) == 0, errors
    
    def validate_batch(self, patients: List[Dict]) -> Dict[str, List]:
        """
        Validate multiple patients.
        
        Args:
            patients: List of patient data dictionaries
            
        Returns:
            Dictionary with 'valid' and 'invalid' lists
        """
        results = {"valid": [], "invalid": []}
        
        for patient in patients:
            is_valid, errors = self.validate(patient)
            if is_valid:
                results["valid"].append(patient)
            else:
                results["invalid"].append({
                    "patient": patient,
                    "errors": errors
                })
        
        return results
    
    def get_validation_summary(self, patients: List[Dict]) -> Dict:
        """
        Get validation summary statistics.
        
        Args:
            patients: List of patient data dictionaries
            
        Returns:
            Dictionary with summary statistics
        """
        results = self.validate_batch(patients)
        
        return {
            "total": len(patients),
            "valid": len(results["valid"]),
            "invalid": len(results["invalid"]),
            "validation_rate": len(results["valid"]) / len(patients) if patients else 0
        }
