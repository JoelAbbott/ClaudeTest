from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class ValidationEntry:
    """Represents a single validation entry (error, warning, or passed)."""
    
    message: str
    column: str
    row: Optional[int] = None
    severity: str = 'error'  # 'error', 'warning', or 'passed'
    value: Optional[Any] = None


class ValidationResult:
    """Stores the results of data validation operations."""
    
    def __init__(self, source_file: str):
        """Initialize validation result for a source file.
        
        Args:
            source_file: Path to the source file being validated.
        """
        self.source_file = source_file
        self.errors: List[ValidationEntry] = []
        self.warnings: List[ValidationEntry] = []
        self.passed: List[ValidationEntry] = []
    
    def add_error(self, message: str, column: str, row: Optional[int] = None, value: Optional[Any] = None) -> None:
        """Add an error to the validation result.
        
        Args:
            message: Description of the error.
            column: Column name where error occurred.
            row: Row number where error occurred (0-indexed).
            value: The problematic value.
        """
        entry = ValidationEntry(
            message=message,
            column=column,
            row=row,
            severity='error',
            value=value
        )
        self.errors.append(entry)
    
    def add_warning(self, message: str, column: str, row: Optional[int] = None, value: Optional[Any] = None) -> None:
        """Add a warning to the validation result.
        
        Args:
            message: Description of the warning.
            column: Column name where warning occurred.
            row: Row number where warning occurred (0-indexed).
            value: The value that triggered the warning.
        """
        entry = ValidationEntry(
            message=message,
            column=column,
            row=row,
            severity='warning',
            value=value
        )
        self.warnings.append(entry)
    
    def add_passed(self, message: str, column: str, row: Optional[int] = None) -> None:
        """Add a passed validation to the result.
        
        Args:
            message: Description of what passed validation.
            column: Column name that passed validation.
            row: Row number that passed validation (0-indexed).
        """
        entry = ValidationEntry(
            message=message,
            column=column,
            row=row,
            severity='passed'
        )
        self.passed.append(entry)
    
    def has_errors(self) -> bool:
        """Check if validation result has any errors.
        
        Returns:
            True if there are errors, False otherwise.
        """
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if validation result has any warnings.
        
        Returns:
            True if there are warnings, False otherwise.
        """
        return len(self.warnings) > 0
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the validation results.
        
        Returns:
            Dictionary containing summary statistics.
        """
        return {
            'source_file': self.source_file,
            'total_errors': len(self.errors),
            'total_warnings': len(self.warnings),
            'total_passed': len(self.passed),
            'total_issues': len(self.errors) + len(self.warnings)
        }