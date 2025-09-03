import pytest
from src.validation_result import ValidationResult, ValidationEntry


class TestValidationResult:
    
    def test_validation_result_initialization(self):
        """Test ValidationResult initialization."""
        result = ValidationResult(source_file='test.xlsx')
        
        assert result.source_file == 'test.xlsx'
        assert result.errors == []
        assert result.warnings == []
        assert result.passed == []
    
    def test_add_error(self):
        """Test adding errors to validation result."""
        result = ValidationResult(source_file='test.xlsx')
        result.add_error('Missing value', 'name', 2)
        
        assert len(result.errors) == 1
        error = result.errors[0]
        assert error.message == 'Missing value'
        assert error.column == 'name'
        assert error.row == 2
        assert error.severity == 'error'
    
    def test_add_warning(self):
        """Test adding warnings to validation result."""
        result = ValidationResult(source_file='test.xlsx')
        result.add_warning('Potential issue', 'age', 5)
        
        assert len(result.warnings) == 1
        warning = result.warnings[0]
        assert warning.message == 'Potential issue'
        assert warning.column == 'age'
        assert warning.row == 5
        assert warning.severity == 'warning'
    
    def test_add_passed(self):
        """Test adding passed validations to result."""
        result = ValidationResult(source_file='test.xlsx')
        result.add_passed('Valid data type', 'id')
        
        assert len(result.passed) == 1
        passed = result.passed[0]
        assert passed.message == 'Valid data type'
        assert passed.column == 'id'
        assert passed.severity == 'passed'
    
    def test_get_summary(self):
        """Test getting validation summary."""
        result = ValidationResult(source_file='test.xlsx')
        result.add_error('Error 1', 'col1', 1)
        result.add_error('Error 2', 'col2', 2)
        result.add_warning('Warning 1', 'col3', 3)
        result.add_passed('Passed 1', 'col4')
        
        summary = result.get_summary()
        
        assert summary['total_errors'] == 2
        assert summary['total_warnings'] == 1
        assert summary['total_passed'] == 1
        assert summary['source_file'] == 'test.xlsx'
    
    def test_validation_entry(self):
        """Test ValidationEntry structure."""
        entry = ValidationEntry(
            message='Test message',
            column='test_col',
            row=1,
            severity='error'
        )
        
        assert entry.message == 'Test message'
        assert entry.column == 'test_col'
        assert entry.row == 1
        assert entry.severity == 'error'
    
    def test_has_errors(self):
        """Test checking if result has errors."""
        result = ValidationResult(source_file='test.xlsx')
        assert not result.has_errors()
        
        result.add_error('Test error', 'col', 1)
        assert result.has_errors()
    
    def test_has_warnings(self):
        """Test checking if result has warnings."""
        result = ValidationResult(source_file='test.xlsx')
        assert not result.has_warnings()
        
        result.add_warning('Test warning', 'col', 1)
        assert result.has_warnings()