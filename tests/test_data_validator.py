import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os

from src.data_validator import DataValidator, ValidationResult


class TestDataValidator:
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return pd.DataFrame({
            'id': [1, 2, 3, None, 5],
            'name': ['Alice', 'Bob', '', 'David', 'Eve'],
            'age': [25, 'invalid', 30, 35, 40],
            'salary': [50000.0, 60000.0, None, 80000.0, 90000.0],
            'department': ['Engineering', 'Sales', 'Engineering', 'HR', 'Sales']
        })
    
    @pytest.fixture
    def temp_excel_file(self, sample_data):
        """Create a temporary Excel file for testing."""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            sample_data.to_excel(tmp.name, index=False)
            yield tmp.name
        os.unlink(tmp.name)
    
    def test_validator_initialization(self):
        """Test DataValidator can be initialized."""
        validator = DataValidator()
        assert validator is not None
    
    def test_detect_missing_values(self, sample_data):
        """Test detection of missing values."""
        validator = DataValidator()
        result = validator.detect_missing_values(sample_data)
        
        assert isinstance(result, ValidationResult)
        assert len(result.errors) > 0
        assert any('id' in error.column for error in result.errors)
        assert any('salary' in error.column for error in result.errors)
    
    def test_detect_data_type_errors(self, sample_data):
        """Test detection of incorrect data types."""
        validator = DataValidator()
        type_rules = {
            'id': 'int',
            'age': 'int', 
            'salary': 'float',
            'name': 'str',
            'department': 'str'
        }
        result = validator.validate_data_types(sample_data, type_rules)
        
        assert isinstance(result, ValidationResult)
        assert len(result.errors) > 0
        assert any('age' in error.column for error in result.errors)
    
    def test_validate_excel_file(self, temp_excel_file):
        """Test validation of an Excel file."""
        validator = DataValidator()
        rules = {
            'required_columns': ['id', 'name', 'age', 'salary', 'department'],
            'data_types': {
                'id': 'int',
                'age': 'int',
                'salary': 'float',
                'name': 'str',
                'department': 'str'
            }
        }
        
        result = validator.validate_file(temp_excel_file, rules)
        assert isinstance(result, ValidationResult)
        assert result.source_file == temp_excel_file
    
    def test_generate_colored_output(self, temp_excel_file):
        """Test generation of color-coded Excel output."""
        validator = DataValidator()
        rules = {
            'data_types': {
                'id': 'int',
                'age': 'int',
                'salary': 'float'
            }
        }
        
        result = validator.validate_file(temp_excel_file, rules)
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as output_file:
            validator.generate_colored_output(result, output_file.name)
            
            # Verify the output file exists and has expected structure
            assert Path(output_file.name).exists()
            
            # Read back and verify structure
            df_summary = pd.read_excel(output_file.name, sheet_name='Summary')
            df_lineage = pd.read_excel(output_file.name, sheet_name='Data_Lineage')
            
            assert not df_summary.empty
            assert not df_lineage.empty
            assert 'source_file' in df_lineage.columns
            
        os.unlink(output_file.name)
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty dataframes."""
        validator = DataValidator()
        empty_df = pd.DataFrame()
        result = validator.detect_missing_values(empty_df)
        
        assert isinstance(result, ValidationResult)
        assert len(result.warnings) > 0
        assert any('empty' in warning.message.lower() for warning in result.warnings)
    
    def test_validation_result_structure(self):
        """Test ValidationResult structure and methods."""
        result = ValidationResult(source_file='test.xlsx')
        
        assert result.source_file == 'test.xlsx'
        assert result.errors == []
        assert result.warnings == []
        assert result.passed == []
        
        result.add_error('Test error', 'column1', 0)
        result.add_warning('Test warning', 'column2', 1)
        result.add_passed('Test passed', 'column3')
        
        assert len(result.errors) == 1
        assert len(result.warnings) == 1
        assert len(result.passed) == 1