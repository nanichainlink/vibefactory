"""Prompt templates for Vibe Coding workflow."""

def create_feature_prompt(feature_name: str, description: str, requirements: list) -> str:
    """Create a prompt for generating a new feature.
    
    Args:
        feature_name: Name of the feature to implement
        description: Detailed description of the feature
        requirements: List of specific requirements/acceptance criteria
        
    Returns:
        Formatted prompt string
    """
    return f"""
# Feature Implementation Request

## Feature: {feature_name}

### Description
{description}

### Requirements
""" + "\n".join(f"- {req}" for req in requirements) + """

### Implementation Guidelines
1. Follow Python best practices and PEP 8 style guide
2. Include type hints for all function signatures
3. Add comprehensive docstrings following Google style
4. Include error handling and input validation
5. Add unit tests for all new functionality
6. Ensure compatibility with existing codebase

### Expected Output
- Implementation in the appropriate module
- Unit tests in the tests/ directory
- Updated documentation in docs/ if needed
"""

def create_test_prompt(module_path: str, function_name: str) -> str:
    """Create a prompt for generating tests for a function.
    
    Args:
        module_path: Path to the module containing the function
        function_name: Name of the function to test
        
    Returns:
        Formatted prompt string
    """
    return f"""
# Test Generation Request

## Module: {module_path}
## Function: {function_name}

Please create comprehensive unit tests for the function mentioned above.

### Guidelines:
1. Test both typical and edge cases
2. Include tests for error conditions
3. Use pytest framework
4. Follow Arrange-Act-Assert pattern
5. Include descriptive test names
6. Ensure high test coverage

### Example Test Structure:
```python
def test_{function_name}_typical_case():
    # Arrange
    # ... setup test data ...
    
    # Act
    # ... call the function ...
    
    # Assert
    # ... verify results ...
```
"""

def create_doc_prompt(component_name: str, component_type: str) -> str:
    """Create a prompt for generating documentation.
    
    Args:
        component_name: Name of the component to document
        component_type: Type of component (e.g., 'module', 'class', 'function')
        
    Returns:
        Formatted prompt string
    """
    return f"""
# Documentation Generation Request

## Component: {component_name}
## Type: {component_type}

Please create comprehensive documentation for the {component_type} mentioned above.

### Documentation Guidelines:
1. Include a clear description of purpose and functionality
2. Document all parameters with their types and descriptions
3. Document return values and exceptions
4. Include usage examples
5. Follow Google style docstrings
6. Keep documentation concise but complete

### Example Format:
```python
"""One-line description.

Extended description with details about the {component_type}.

Args:
    param1 (type): Description of param1.
    param2 (type, optional): Description of param2. Defaults to None.

Returns:
    type: Description of return value.

Raises:
    ErrorType: When something goes wrong.

Example:
    >>> example_usage()
    expected_result
"""
```
"""
