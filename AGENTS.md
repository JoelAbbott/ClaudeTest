---

## 🚀 Project Overview

This document serves as the single source of truth for Claude Code when interacting with this codebase. The goal is to develop a robust, enterprise-grade data validation application using the `pandas` library, designed to address common data governance tasks. The application will feature a command-line interface (CLI) driven by explicit `/commands` and maintain session state for comprehensive reporting.

### Core Functionality
The app will address real-world data reconciliation challenges [5]. It will validate data types, value ranges, regex patterns, perform cross-column validation, check referential integrity, and handle inconsistent data entries and missing values.

### Input & Output Specifications
*   **Input**: Multiple Excel (.xlsx) and CSV (.csv) files containing deliberate "bad data" (e.g., missing values, inconsistent naming, incorrect data types, duplicate rows, trailing spaces, case sensitivity issues) [7].
*   **Output**: A new Excel spreadsheet with multiple tabs (Summary, Data_Lineage, validation tasks) using color-coding (red for errors, yellow for warnings, green for passed). Output should support alternative formats like CSV and HTML. A `Data_Lineage` tab should track source files for each data point.
*   **Session Management**: Results from each command are stored in a `.session/` directory as JSON files for persistence, enabling comprehensive reporting across commands.

### Technology Stack
*   **Primary Language**: Python
*   **Core Library**: `pandas`
*   **Dependencies**: `openpyxl`, `tqdm`, `colorama`, `pytest`, `memory-profiler`, `argparse`, `json`, `logging`, `os`, `pathlib`.
*   **System Requirements**: Python 3.8+, 4GB RAM (8GB recommended), 500MB+ disk space.

---

## 💻 Coding Standards and Best Practices

**You MUST adhere to the following coding standards to ensure high-quality, maintainable code.**

### General Principles
*   **Readability**: Prioritize clear and understandable code.
*   **Performance**: Consider execution time and memory usage for operations, especially with large datasets.
*   **Error Handling**: Implement robust error handling mechanisms, providing clear feedback messages for users. Examples: `"[FILE NOT FOUND] Cannot read 'sales.xlsx'. Suggestion: Check the file path and ensure the file exists."`.
*   **Documentation**: All functions, classes, and complex logic blocks must include clear docstrings (Google style recommended) and comments.
*   **Design Patterns**: Follow best practices like SOLID and DRY principles.
*   **Type Hints**: Use Python type hints for improved code clarity and maintainability.
*   **Modularity**: Design focused components with single, clear responsibilities to improve performance and predictability.

### Specific Guidelines
*   **File Naming**: Use `snake_case` for Python file names.
*   **Variable/Function Naming**: Use descriptive names that clearly indicate their purpose.
*   **Code Formatting**: Use a consistent formatter (e.g., Black) to ensure uniform code style.
*   **Imports**: Destructure imports when possible (e.g., `from library import foo`).
*   **Avoid Irreversible Actions**: Do not take irreversible actions that might harm the user or their environment without explicit user approval.
*   **Context Preservation**: When creating code, ensure new implementations don't conflict with existing patterns or inadvertently overwrite critical sections.

---

## ✅ Testing Strategy

**All new features and bug fixes MUST be accompanied by comprehensive test coverage.**

### General Principles
*   **Test-Driven Development (TDD)**: Whenever possible, write tests based on expected input/output pairs *before* implementing the code. Ensure tests fail initially and then pass once the code is written.
*   **Unit Tests**: Use `pytest` for unit testing. New features require corresponding unit tests.
*   **Edge Cases**: Include test cases for valid inputs, invalid inputs, and edge cases (e.g., empty files, huge files, malformed data).
*   **Test Execution**: To run tests, use `pytest -v`.
*   **Verification**: After implementing a solution, ensure it passes all relevant tests. Do not overfit to tests.
*   **Blind Validation**: For critical tasks, a separate agent or mechanism should be used for blind validation to verify that the main agent's work is reliably done and the tests pass.

### Performance Testing
*   **Profiling**: Conduct memory profiling for optimization and monitor execution time for individual commands.
*   **Large Files**: Implement chunk processing for files larger than 100MB.
*   **Progress Bars**: Use `tqdm` for long-running operations to provide user feedback.

---

## 🔄 Workflow and Git Practices

**Follow these guidelines for effective collaboration and version control.**

### Git Workflow
*   **Branching**: Use a clear branching strategy (e.g., `feature/branch-name`, `bugfix/branch-name`).
*   **Commit Messages**: Write descriptive commit messages that clearly explain the changes made. Claude should automatically compose messages based on diff and context.
*   **Pull Requests**: Claude can assist in creating and reviewing pull requests. Ensure PRs include sufficient context and testing details.
*   **Sensitive Files**: Always ensure sensitive files (e.g., `.env`, `package-lock.json`, `.git/`) are correctly excluded from version control using `.gitignore`.

### Command-Line Interface (CLI)
*   The application is command-line interface driven by explicit `/commands`.
*   **Session Reset**: Use `/clear` frequently between tasks to reset the context window and maintain focus [29].
*   **Debugging**: When debugging, you may be asked to capture error messages and stack traces, identify reproduction steps, isolate failures, implement minimal fixes, and verify solutions.
*   **Help**: The `/help` command shows all available commands with examples.

### Common Commands to Document and Use:
*   `/compare --files <list of files> --primary-key <column name>`: Finds missing records between files.
*   `/merge --files <list of files> --column-map <JSON mapping> --strategy <how to combine data>`: Combines multiple files into one, standardizing column names.
*   `/validate --file <file to validate> --rules <JSON string defining rules>`: Checks data quality against specified rules.
*   `/report --output-file <name for the report file> --format <output format>`: Generates a comprehensive report of all issues found.
*   `/preview --file <file to preview> --rows <number of rows>`: Shows the first few rows of a file.
*   `/status`: Displays all issues found so far in the current session.
*   `/clear`: Resets all findings and starts a new validation session.
*   `/help` or `/help --command validate`: Gets command assistance.

---

## 🛠️ Developer Environment

**Ensure your development environment is set up consistently.**

### Tools
*   **Git**: Installed and configured locally.
*   **Google Cloud CLI**: Installed and logged in (for Jules integration).
*   **GitHub CLI (`gh`)**: Installed to allow Claude to interact with GitHub.
*   **Python Virtual Environments**: Always create and activate a virtual environment within the repository.
*   **Package Manager**: Use `pip` for Python package management.
*   **Verification Script**: Use `verify_environment.py` (if available) to automatically check for all required installations.

### Data Generation
*   Create a `create_test_data.py` file to generate test data with deliberate data quality issues.

---

## ⚠️ Specific Project Notes and Warnings

*   **Model Chattyness**: Claude models can be chatty. Specify the desired output format explicitly, perhaps by using an assistant message to ensure consistent responses.
*   **Hallucination Prevention**: Allow Claude to state "I don't know" to prevent it from generating inaccurate information.
*   **Clarity and Specificity**: Be direct, concise, and specific in your instructions, especially for complex tasks. The more detailed the instructions, the better the results.
*   **Iterative Refinement**: Start with simple prompts and gradually refine them based on the output. Adjust prompt length, wording, or structure if initial results are not satisfactory.
*   **External Data**: When dealing with external data, prioritize using tools like `perplexity` for deep research to get the latest documentation, as LLM knowledge cutoffs can lead to outdated information .

---

## 🎯 Task-Specific Guidance

### For Designers (if applicable to this project)
*   **Detailed Explanations**: When assisting designers with limited coding experience, provide detailed explanations and suggest smaller, incremental changes.
*   **Image Analysis**: Leverage image pasting for prototyping; Claude excels at reading designs and generating functional code.

### For Data Scientists (if applicable to this project)
*   **Codebase Comprehension**: Utilize Claude for codebase exploration, understanding data pipeline dependencies, and identifying relevant files.
*   **ML Concept Explanation**: Ask Claude to explain model-specific functions and settings to bridge knowledge gaps.