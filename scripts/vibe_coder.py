"""
Vibe Coder - Automated code generation and documentation tool.

This script provides functionality to generate code, tests, and documentation
using AI-powered prompts based on the Vibe Coding methodology.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vibe_coder.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import prompt templates
try:
    from ..windsurf.templates.prompt_template import (
        create_feature_prompt,
        create_test_prompt,
        create_doc_prompt
    )
    logger.info("Successfully imported prompt templates")
except ImportError as e:
    logger.warning(f"Could not import prompt templates: {e}")
    logger.warning("Using fallback prompt templates")
    
    # Fallback prompt templates
    def create_feature_prompt(*args, **kwargs):
        return "Feature implementation prompt template not found"
    
    def create_test_prompt(*args, **kwargs):
        return "Test generation prompt template not found"
    
    def create_doc_prompt(*args, **kwargs):
        return "Documentation generation prompt template not found"


class VibeCoder:
    """Main class for Vibe Coding automation."""
    
    def __init__(self, config_path: str = None):
        """Initialize the VibeCoder with optional configuration.
        
        Args:
            config_path: Path to configuration file (JSON or YAML)
        """
        self.config = self._load_config(config_path)
        logger.info("VibeCoder initialized")
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Dictionary containing configuration
        """
        default_config = {
            "ai_model": "gpt-4",
            "temperature": 0.2,
            "max_tokens": 2000,
            "code_style": "pep8",
            "test_framework": "pytest",
            "doc_style": "google"
        }
        
        if not config_path:
            logger.info("Using default configuration")
            return default_config
            
        config_path = Path(config_path)
        if not config_path.exists():
            logger.warning(f"Config file {config_path} not found. Using defaults.")
            return default_config
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.suffix.lower() == '.json':
                    config = json.load(f)
                else:
                    import yaml
                    config = yaml.safe_load(f)
            
            # Merge with defaults
            for key, value in default_config.items():
                config.setdefault(key, value)
                
            logger.info(f"Loaded configuration from {config_path}")
            return config
            
        except Exception as e:
            logger.error(f"Error loading config from {config_path}: {e}")
            return default_config
    
    def generate_feature(self, feature_name: str, description: str, requirements: List[str]) -> str:
        """Generate code for a new feature.
        
        Args:
            feature_name: Name of the feature to implement
            description: Detailed description of the feature
            requirements: List of specific requirements/acceptance criteria
            
        Returns:
            Generated code as a string
        """
        logger.info(f"Generating feature: {feature_name}")
        prompt = create_feature_prompt(feature_name, description, requirements)
        return self._call_ai(prompt)
    
    def generate_tests(self, module_path: str, function_name: str) -> str:
        """Generate tests for a function.
        
        Args:
            module_path: Path to the module containing the function
            function_name: Name of the function to test
            
        Returns:
            Generated test code as a string
        """
        logger.info(f"Generating tests for {function_name} in {module_path}")
        prompt = create_test_prompt(module_path, function_name)
        return self._call_ai(prompt)
    
    def generate_docs(self, component_name: str, component_type: str) -> str:
        """Generate documentation for a component.
        
        Args:
            component_name: Name of the component to document
            component_type: Type of component (e.g., 'module', 'class', 'function')
            
        Returns:
            Generated documentation as a string
        """
        logger.info(f"Generating docs for {component_type}: {component_name}")
        prompt = create_doc_prompt(component_name, component_type)
        return self._call_ai(prompt)
    
    def _call_ai(self, prompt: str) -> str:
        """Call the AI model to generate a response.
        
        Args:
            prompt: The prompt to send to the AI
            
        Returns:
            The AI's response as a string
        """
        # This is a placeholder for the actual AI call
        # In a real implementation, this would call an AI API
        logger.debug(f"Sending prompt to AI: {prompt[:100]}...")
        
        # Simulate AI response for now
        return f"""# AI-Generated Response

This is a placeholder response. In a real implementation, this would be generated by an AI model.

Prompt was: {prompt[:200]}...
"""

def main():
    """Main entry point for the Vibe Coder CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Vibe Coder - Automated code generation and documentation')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Feature generation command
    feature_parser = subparsers.add_parser('feature', help='Generate a new feature')
    feature_parser.add_argument('name', help='Name of the feature')
    feature_parser.add_argument('description', help='Description of the feature')
    feature_parser.add_argument('--requirements', nargs='+', help='List of requirements', default=[])
    
    # Test generation command
    test_parser = subparsers.add_parser('test', help='Generate tests')
    test_parser.add_argument('module', help='Path to the module')
    test_parser.add_argument('function', help='Name of the function to test')
    
    # Documentation generation command
    doc_parser = subparsers.add_parser('doc', help='Generate documentation')
    doc_parser.add_argument('component', help='Name of the component to document')
    doc_parser.add_argument('--type', choices=['module', 'class', 'function'], default='function',
                          help='Type of component (default: function)')
    
    # Common arguments
    for p in [parser, feature_parser, test_parser, doc_parser]:
        p.add_argument('--config', help='Path to configuration file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    coder = VibeCoder(args.config)
    
    try:
        if args.command == 'feature':
            result = coder.generate_feature(args.name, args.description, args.requirements)
        elif args.command == 'test':
            result = coder.generate_tests(args.module, args.function)
        elif args.command == 'doc':
            result = coder.generate_docs(args.component, args.type)
        else:
            logger.error(f"Unknown command: {args.command}")
            return
        
        print("\n" + "="*80)
        print(result)
        print("="*80 + "\n")
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
