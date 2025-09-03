import pytest
import tempfile
import os
import json
from pathlib import Path
import pandas as pd

from src.cli import CLI, CommandParser


class TestCLI:
    
    @pytest.fixture
    def cli_instance(self):
        """Create a CLI instance for testing."""
        return CLI()
    
    @pytest.fixture
    def sample_excel_file(self):
        """Create a sample Excel file for testing."""
        data = pd.DataFrame({
            'id': [1, 2, None, 4],
            'name': ['Alice', 'Bob', 'Charlie', ''],
            'age': [25, 'invalid', 30, 35]
        })
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            data.to_excel(tmp.name, index=False)
            yield tmp.name
        os.unlink(tmp.name)
    
    def test_command_parser_initialization(self):
        """Test CommandParser can be initialized."""
        parser = CommandParser()
        assert parser is not None
    
    def test_parse_validate_command(self):
        """Test parsing of /validate command."""
        parser = CommandParser()
        command_str = '/validate --file test.xlsx --rules \'{"data_types": {"id": "int"}}\''
        
        command, args = parser.parse_command(command_str)
        
        assert command == 'validate'
        assert args['file'] == 'test.xlsx'
        assert isinstance(args['rules'], dict)
        assert 'data_types' in args['rules']
    
    def test_validate_command_execution(self, cli_instance, sample_excel_file):
        """Test execution of validate command."""
        rules = {
            'data_types': {
                'id': 'int',
                'age': 'int',
                'name': 'str'
            }
        }
        
        result = cli_instance.execute_validate(sample_excel_file, rules)
        
        assert result is not None
        assert 'output_file' in result
        assert Path(result['output_file']).exists()
        
        # Clean up
        os.unlink(result['output_file'])
    
    def test_help_command(self, cli_instance):
        """Test help command functionality."""
        help_text = cli_instance.show_help()
        
        assert isinstance(help_text, str)
        assert '/validate' in help_text
        assert '--file' in help_text
        assert '--rules' in help_text
    
    def test_session_management(self, cli_instance):
        """Test session state management."""
        # Test session directory creation
        session_dir = cli_instance.get_session_dir()
        assert Path(session_dir).exists()
        
        # Test saving session data
        test_data = {'test': 'data'}
        cli_instance.save_session_data('test_session.json', test_data)
        
        saved_file = Path(session_dir) / 'test_session.json'
        assert saved_file.exists()
        
        # Test loading session data
        loaded_data = cli_instance.load_session_data('test_session.json')
        assert loaded_data == test_data
    
    def test_invalid_command_handling(self):
        """Test handling of invalid commands."""
        parser = CommandParser()
        
        with pytest.raises(ValueError):
            parser.parse_command('/invalid_command')
    
    def test_missing_file_handling(self, cli_instance):
        """Test handling of missing input files."""
        result = cli_instance.execute_validate('nonexistent.xlsx', {})
        assert 'error' in result
        assert 'File not found' in result['error']