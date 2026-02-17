"""Clinical trial protocol parser."""

import re
from typing import Dict, List, Optional


class ProtocolParser:
    """Parses clinical trial protocol documents."""
    
    def __init__(self):
        """Initialize parser."""
        self.protocol_data = {}
    
    def extract_inclusion_criteria(self, protocol_text: str) -> List[str]:
        """
        Extract inclusion criteria from protocol text.
        
        Args:
            protocol_text: Full protocol document text
            
        Returns:
            List of inclusion criteria
        """
        # Simple pattern matching for demonstration
        pattern = r"Inclusion Criteria?:?\s*(.*?)(?=Exclusion Criteria|$)"
        match = re.search(pattern, protocol_text, re.IGNORECASE | re.DOTALL)
        
        if not match:
            return []
        
        criteria_text = match.group(1)
        criteria = [c.strip() for c in re.split(r'\n\d+\.|\n-', criteria_text) if c.strip()]
        
        return criteria
    
    def extract_exclusion_criteria(self, protocol_text: str) -> List[str]:
        """
        Extract exclusion criteria from protocol text.
        
        Args:
            protocol_text: Full protocol document text
            
        Returns:
            List of exclusion criteria
        """
        pattern = r"Exclusion Criteria?:?\s*(.*?)(?=\n\n[A-Z]|$)"
        match = re.search(pattern, protocol_text, re.IGNORECASE | re.DOTALL)
        
        if not match:
            return []
        
        criteria_text = match.group(1)
        criteria = [c.strip() for c in re.split(r'\n\d+\.|\n-', criteria_text) if c.strip()]
        
        return criteria
    
    def extract_protocol_number(self, protocol_text: str) -> Optional[str]:
        """
        Extract protocol number from document.
        
        Args:
            protocol_text: Full protocol document text
            
        Returns:
            Protocol number or None
        """
        pattern = r"Protocol\s+(?:Number|ID|#):?\s*([A-Z0-9-]+)"
        match = re.search(pattern, protocol_text, re.IGNORECASE)
        
        return match.group(1) if match else None
    
    def parse_protocol(self, protocol_text: str) -> Dict:
        """
        Parse full protocol document.
        
        Args:
            protocol_text: Full protocol document text
            
        Returns:
            Dictionary with parsed protocol data
        """
        return {
            "protocol_number": self.extract_protocol_number(protocol_text),
            "inclusion_criteria": self.extract_inclusion_criteria(protocol_text),
            "exclusion_criteria": self.extract_exclusion_criteria(protocol_text)
        }
