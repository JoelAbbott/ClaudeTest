import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import logging
import pandas as pd

from .data_validator import DataValidator
from .validation_result import ValidationResult


class CommandParser:
    """Parses CLI commands for the data validation application."""
    
    def __init__(self):
        """Initialize the command parser."""
        self.commands = {
            'validate': self._parse_validate_command,
            'help': self._parse_help_command,
            'clear': self._parse_clear_command,
            'status': self._parse_status_command
        }
    
    def parse_command(self, command_str: str) -> Tuple[str, Dict[str, Any]]:
        """Parse a command string into command and arguments.
        
        Args:
            command_str: Command string starting with '/'.
            
        Returns:
            Tuple of (command_name, arguments_dict).
            
        Raises:
            ValueError: If command is invalid or malformed.
        """
        if not command_str.startswith('/'):
            raise ValueError("Commands must start with '/'")
        
        parts = command_str[1:].split(' ', 1)
        command = parts[0].lower()
        
        if command not in self.commands:
            raise ValueError(f"Unknown command: {command}")
        
        args_str = parts[1] if len(parts) > 1 else ''
        return command, self.commands[command](args_str)
    
    def _parse_validate_command(self, args_str: str) -> Dict[str, Any]:
        """Parse validate command arguments."""
        import shlex
        
        # Use shlex to properly handle quoted JSON strings
        try:
            args_list = shlex.split(args_str) if args_str else []
        except ValueError as e:
            raise ValueError(f"Invalid command syntax: {str(e)}")
        
        parser = argparse.ArgumentParser(description='Validate data file', prog='validate')
        parser.add_argument('--file', required=True, help='Path to file to validate')
        parser.add_argument('--rules', required=True, help='JSON string with validation rules')
        parser.add_argument('--output', help='Output file path (optional)')
        
        try:
            args = parser.parse_args(args_list)
            rules = json.loads(args.rules)
            
            return {
                'file': args.file,
                'rules': rules,
                'output': args.output
            }
        except (json.JSONDecodeError, SystemExit) as e:
            raise ValueError(f"Invalid validate command arguments: {str(e)}")
    
    def _parse_help_command(self, args_str: str) -> Dict[str, Any]:
        """Parse help command arguments."""
        parser = argparse.ArgumentParser(description='Show help')
        parser.add_argument('--command', help='Show help for specific command')
        
        try:
            args = parser.parse_args(args_str.split() if args_str else [])
            return {'command': args.command}
        except argparse.ArgumentError:
            return {}
    
    def _parse_clear_command(self, args_str: str) -> Dict[str, Any]:
        """Parse clear command arguments."""
        return {}
    
    def _parse_status_command(self, args_str: str) -> Dict[str, Any]:
        """Parse status command arguments."""
        return {}


class CLI:
    """Command-line interface for the data validation application."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.parser = CommandParser()
        self.validator = DataValidator()
        self.session_dir = Path('.session')
        self.session_dir.mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def execute_command(self, command_str: str) -> Dict[str, Any]:
        """Execute a CLI command.
        
        Args:
            command_str: Command string to execute.
            
        Returns:
            Dictionary containing execution results.
        """
        try:
            command, args = self.parser.parse_command(command_str)
            
            if command == 'validate':
                return self.execute_validate(args['file'], args['rules'], args.get('output'))
            elif command == 'help':
                return {'help_text': self.show_help(args.get('command'))}
            elif command == 'clear':
                return self.clear_session()
            elif command == 'status':
                return self.show_status()
            else:
                raise ValueError(f"Command not implemented: {command}")
                
        except Exception as e:
            self.logger.error(f"Command execution failed: {str(e)}")
            return {'error': str(e)}
    
    def execute_validate(self, file_path: str, rules: Dict[str, Any], output_path: Optional[str] = None) -> Dict[str, Any]:
        """Execute the validate command.
        
        Args:
            file_path: Path to file to validate.
            rules: Validation rules dictionary.
            output_path: Optional output file path.
            
        Returns:
            Dictionary containing validation results.
        """
        try:
            # Perform validation
            result = self.validator.validate_file(file_path, rules)
            
            # Generate output file path if not provided
            if output_path is None:
                input_path = Path(file_path)
                output_path = str(input_path.parent / f"{input_path.stem}_validated.xlsx")
            
            # Generate colored Excel output
            self.validator.generate_colored_output(result, output_path)
            
            # Save session data
            session_file = f"validate_{Path(file_path).stem}.json"
            self.save_session_data(session_file, {
                'source_file': file_path,
                'output_file': output_path,
                'summary': result.get_summary(),
                'timestamp': pd.Timestamp.now().isoformat()
            })
            
            return {
                'success': True,
                'output_file': output_path,
                'summary': result.get_summary(),
                'message': f'Validation complete. Results saved to {output_path}'
            }
            
        except Exception as e:
            self.logger.error(f"Validation failed: {str(e)}")
            return {'error': str(e)}
    
    def show_help(self, command: Optional[str] = None) -> str:
        """Show help information.
        
        Args:
            command: Optional specific command to show help for.
            
        Returns:
            Help text string.
        """
        if command == 'validate':
            return """
/validate - Validate data quality in Excel/CSV files

Usage: /validate --file <path> --rules <json_rules> [--output <path>]

Arguments:
  --file     Path to Excel (.xlsx) or CSV (.csv) file to validate
  --rules    JSON string containing validation rules
  --output   Optional output file path (defaults to <filename>_validated.xlsx)

Rules format:
{
  "required_columns": ["col1", "col2"],
  "data_types": {
    "col1": "int",
    "col2": "str",
    "col3": "float"
  }
}

Example:
/validate --file data.xlsx --rules '{"data_types": {"id": "int", "name": "str"}}'
"""
        
        return """
Data Validation CLI - Available Commands:

/validate --file <path> --rules <json_rules> [--output <path>]
    Validate data quality in Excel/CSV files
    
/help [--command <command_name>]
    Show this help or help for a specific command
    
/clear
    Clear current session and reset validation state
    
/status
    Show current session status and findings

Use /help --command <command_name> for detailed help on specific commands.
"""
    
    def clear_session(self) -> Dict[str, Any]:
        """Clear the current session.
        
        Returns:
            Dictionary containing clear operation results.
        """
        try:
            # Remove all session files
            for file_path in self.session_dir.glob('*.json'):
                file_path.unlink()
            
            return {
                'success': True,
                'message': 'Session cleared successfully'
            }
        except Exception as e:
            return {'error': f'Failed to clear session: {str(e)}'}
    
    def show_status(self) -> Dict[str, Any]:
        """Show current session status.
        
        Returns:
            Dictionary containing session status information.
        """
        try:
            session_files = list(self.session_dir.glob('*.json'))
            
            if not session_files:
                return {
                    'message': 'No active session data',
                    'session_files': []
                }
            
            session_info = []
            for file_path in session_files:
                data = self.load_session_data(file_path.name)
                if data:
                    session_info.append(data)
            
            return {
                'success': True,
                'session_files': len(session_files),
                'session_data': session_info
            }
            
        except Exception as e:
            return {'error': f'Failed to get status: {str(e)}'}
    
    def get_session_dir(self) -> str:
        """Get the session directory path.
        
        Returns:
            String path to session directory.
        """
        return str(self.session_dir)
    
    def save_session_data(self, filename: str, data: Dict[str, Any]) -> None:
        """Save data to session file.
        
        Args:
            filename: Name of the session file.
            data: Data to save.
        """
        file_path = self.session_dir / filename
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_session_data(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load data from session file.
        
        Args:
            filename: Name of the session file.
            
        Returns:
            Loaded data or None if file doesn't exist.
        """
        file_path = self.session_dir / filename
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load session data: {str(e)}")
            return None


def main():
    """Main entry point for the CLI application."""
    cli = CLI()
    
    print("Data Validation CLI")
    print("Type /help for available commands or /validate to start validation")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            command_str = input("\n> ").strip()
            
            if not command_str:
                continue
            
            if command_str.lower() in ['exit', 'quit']:
                break
            
            result = cli.execute_command(command_str)
            
            if 'error' in result:
                print(f"Error: {result['error']}")
            elif 'help_text' in result:
                print(result['help_text'])
            elif 'message' in result:
                print(result['message'])
            else:
                print("Command executed successfully")
                if 'summary' in result:
                    summary = result['summary']
                    print(f"Errors: {summary['total_errors']}, "
                          f"Warnings: {summary['total_warnings']}, "
                          f"Passed: {summary['total_passed']}")
    
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)


if __name__ == '__main__':
    main()