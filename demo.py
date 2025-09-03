#!/usr/bin/env python3
"""Demonstration script for the data validation application."""

import pandas as pd
from src.cli import CLI


def create_demo_data():
    """Create demonstration data with various validation issues."""
    data = pd.DataFrame({
        'employee_id': [1, 2, 3, None, 5, 'invalid'],
        'name': ['Alice Johnson', 'Bob Smith', '', 'David Wilson', 'Eve Brown', 'Frank Miller'],
        'age': [25, 'thirty', 30, 35, -5, 40],
        'salary': [50000.0, 60000.0, None, 80000.0, 90000.0, 'high'],
        'department': ['Engineering', 'Sales', 'Engineering', 'HR', '', 'Marketing']
    })
    
    data.to_excel('demo_data.xlsx', index=False)
    print("Created demo_data.xlsx with validation issues")
    return 'demo_data.xlsx'


def run_validation_demo():
    """Run a demonstration of the validation functionality."""
    print("🔍 Data Validation Application Demo")
    print("=" * 40)
    
    # Create demo data
    demo_file = create_demo_data()
    
    # Initialize CLI
    cli = CLI()
    
    # Define validation rules
    rules = {
        'required_columns': ['employee_id', 'name', 'age', 'salary', 'department'],
        'data_types': {
            'employee_id': 'int',
            'age': 'int',
            'salary': 'float',
            'name': 'str',
            'department': 'str'
        }
    }
    
    print(f"\n📁 Validating file: {demo_file}")
    print("🔧 Validation rules:")
    print(f"   - Required columns: {rules['required_columns']}")
    print(f"   - Data types: {rules['data_types']}")
    
    # Execute validation
    result = cli.execute_validate(demo_file, rules)
    
    print(f"\n📊 Validation Results:")
    if result.get('success'):
        summary = result['summary']
        print(f"   ❌ Errors: {summary['total_errors']}")
        print(f"   ⚠️  Warnings: {summary['total_warnings']}")
        print(f"   ✅ Passed: {summary['total_passed']}")
        print(f"   📄 Output saved to: {result['output_file']}")
        
        print(f"\n🎨 Output file includes:")
        print(f"   - Validated_Data tab with color-coded cells")
        print(f"   - Summary tab with all validation findings")
        print(f"   - Data_Lineage tab tracking source file information")
        
    else:
        print(f"   ❌ Validation failed: {result.get('error')}")


if __name__ == '__main__':
    run_validation_demo()