"""Adverse event data processor for clinical trials."""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional


class AdverseEventProcessor:
    """Processes and categorizes adverse event data."""
    
    SEVERITY_LEVELS = ["Mild", "Moderate", "Severe", "Life-threatening", "Fatal"]
    REQUIRED_COLUMNS = ["event_id", "patient_id", "event_date", "description", "severity"]
    
    def __init__(self):
        """Initialize processor."""
        self.events = []
    
    def load_events(self, file_path: str) -> pd.DataFrame:
        """
        Load adverse events from CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            DataFrame with adverse events
            
        Raises:
            ValueError: If required columns are missing
        """
        df = pd.read_csv(file_path)
        
        missing_cols = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        return df
    
    def validate_event(self, event: Dict) -> Tuple[bool, List[str]]:
        """
        Validate a single adverse event.
        
        Args:
            event: Dictionary containing event data
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Check required fields
        for field in self.REQUIRED_COLUMNS:
            if field not in event or event[field] is None or event[field] == "":
                errors.append(f"Missing required field: {field}")
        
        # Validate severity
        if "severity" in event and event["severity"] not in self.SEVERITY_LEVELS:
            errors.append(f"Invalid severity: {event['severity']}. Must be one of {self.SEVERITY_LEVELS}")
        
        # Validate date
        if "event_date" in event:
            try:
                event_date = pd.to_datetime(event["event_date"])
                if event_date > pd.Timestamp.now():
                    errors.append("event_date: Cannot be in the future")
            except:
                errors.append("event_date: Invalid date format")
        
        # Validate patient_id format
        if "patient_id" in event:
            if not isinstance(event["patient_id"], str) or not event["patient_id"].startswith("PAT"):
                errors.append("patient_id: Must be string starting with 'PAT'")
        
        return len(errors) == 0, errors
    
    def categorize_by_severity(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Categorize events by severity level.
        
        Args:
            df: DataFrame with adverse events
            
        Returns:
            Dictionary with counts per severity level
        """
        return df["severity"].value_counts().to_dict()
    
    def get_events_by_patient(self, df: pd.DataFrame, patient_id: str) -> pd.DataFrame:
        """
        Get all events for a specific patient.
        
        Args:
            df: DataFrame with adverse events
            patient_id: Patient identifier
            
        Returns:
            Filtered DataFrame
        """
        return df[df["patient_id"] == patient_id]
    
    def calculate_event_rate(self, df: pd.DataFrame, days: int = 30) -> float:
        """
        Calculate adverse event rate per time period.
        
        Args:
            df: DataFrame with adverse events
            days: Number of days for rate calculation
            
        Returns:
            Event rate (events per day)
        """
        if len(df) == 0:
            return 0.0
        
        df["event_date"] = pd.to_datetime(df["event_date"])
        date_range = (df["event_date"].max() - df["event_date"].min()).days
        
        if date_range == 0:
            return len(df)
        
        return len(df) / date_range
