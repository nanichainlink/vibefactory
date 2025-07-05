"""
Documentation Generator for Vibe Coding Workflow

This script automatically generates documentation from docstrings in the codebase
using mkdocs and mkdocstrings.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("doc_generation.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class DocumentationGenerator:
    """Generates documentation from Python docstrings."""

    def __init__(self, project_root: str = ".", docs_dir: str = "docs"):
        """Initialize the DocumentationGenerator.
        
        Args:
            project_root: Root directory of the project
            docs_dir: Directory to store documentation (default: 'docs')
        """
        self.project_root = Path(project_root).resolve()
        self.docs_dir = Path(docs_dir).resolve()
        self.mkdocs_config = self.docs_dir / "mkdocs.yml"
        
        # Create docs directory if it doesn't exist
        self.docs_dir.mkdir(exist_ok=True)
        
        # Documentation structure
        self.pages = {
            "Home": "index.md",
            "API Reference": [
                {"Modules": [
                    {"gps_logic": "api/gps_logic.md"},
                    {"app": "api/app.md"}
                ]}
            ],
            "Guides": [
                "guides/getting_started.md",
                "guides/development_workflow.md"
            ],
            "Changelog": "changelog.md"
        }
        
        # Default mkdocs configuration
        self.default_config = {
            "site_name": "GPS Application",
            "site_url": "https://example.com",
            "repo_url": "https://github.com/yourusername/gps-app",
            "theme": {
                "name": "material",
                "features": [
                    "navigation.tabs",
                    "navigation.indexes",
                    "navigation.sections",
                    "navigation.top"
                ],
                "palette": [
                    {
                        "scheme": "default",
                        "primary": "blue",
                        "accent": "light-blue",
                        "toggle": {
                            "icon": "material/toggle-switch-off-outline",
                            "name": "Switch to dark mode"
                        }
                    },
                    {
                        "scheme": "slate",
                        "primary": "blue",
                        "accent": "light-blue",
                        "toggle": {
                            "icon": "material/toggle-switch",
                            "name": "Switch to light mode"
                        }
                    }
                ]
            },
            "markdown_extensions": [
                "admonition",
                "tables",
                "pymdownx.highlight",
                "pymdownx.superfences",
                "pymdownx.inlinehilite",
                "pymdownx.emoji",
                "pymdownx.tabbed",
                "pymdownx.snippets",
                "pymdownx.arithmatex",
                "pymdownx.details",
                "pymdownx.mark"
            ],
            "plugins": [
                "search",
                "mkdocstrings",
                "mkdocstrings.handlers.python"
            ],
            "nav": []
        }
    
    def initialize_docs(self) -> None:
        """Initialize the documentation structure."""
        logger.info("Initializing documentation structure...")
        
        # Create necessary directories
        (self.docs_dir / "docs" / "api").mkdir(parents=True, exist_ok=True)
        (self.docs_dir / "docs" / "guides").mkdir(parents=True, exist_ok=True)
        
        # Create default files if they don't exist
        self._create_file_if_not_exists("docs/index.md", self._get_index_content())
        self._create_file_if_not_exists("docs/changelog.md", "# Changelog\n\n## [Unreleased]\n\n### Added\n- Initial project setup\n")
        self._create_file_if_not_exists("docs/guides/getting_started.md", "# Getting Started\n\n## Installation\n\n```bash\npip install -r requirements.txt\n```\n\n## Running the Application\n\n```bash\nstreamlit run app.py\n```")
        self._create_file_if_not_exists("docs/guides/development_workflow.md", "# Development Workflow\n\n## Vibe Coding\n\nThis project follows the Vibe Coding methodology.\n\n### Key Principles\n- Automated testing\n- Continuous integration\n- Documentation as code\n- Consistent code style")
        
        # Generate API documentation stubs
        self._generate_api_docs()
        
        # Generate mkdocs.yml if it doesn't exist
        if not self.mkdocs_config.exists():
            self._generate_mkdocs_config()
        
        logger.info("Documentation structure initialized")
    
    def generate_docs(self, serve: bool = False, strict: bool = False) -> bool:
        """Generate the documentation.
        
        Args:
            serve: If True, serve the documentation locally
            strict: If True, fail on warnings
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info("Generating documentation...")
        
        try:
            # Build the documentation
            cmd = ["mkdocs", "build", "--clean", "--site-dir", "_build"]
            if strict:
                cmd.append("--strict")
            
            result = subprocess.run(
                cmd,
                cwd=self.docs_dir,
                check=True,
                capture_output=True,
                text=True
            )
            
            logger.info("Documentation generated successfully")
            
            # Serve the documentation if requested
            if serve:
                self.serve_docs()
                
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error generating documentation: {e}")
            logger.error(f"stdout: {e.stdout}")
            logger.error(f"stderr: {e.stderr}")
            return False
    
    def serve_docs(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """Serve the documentation locally.
        
        Args:
            host: Host to serve on (default: '127.0.0.1')
            port: Port to serve on (default: 8000)
        """
        logger.info(f"Serving documentation at http://{host}:{port}")
        
        try:
            subprocess.run(
                ["mkdocs", "serve", "--dev-addr", f"{host}:{port}"],
                cwd=self.docs_dir,
                check=True
            )
        except KeyboardInterrupt:
            logger.info("Documentation server stopped")
        except Exception as e:
            logger.error(f"Error serving documentation: {e}")
    
    def _generate_api_docs(self) -> None:
        """Generate API documentation stubs."""
        # Generate documentation for gps_logic.py
        self._create_file_if_not_exists(
            "docs/api/gps_logic.md",
            "# gps_logic\n\n::: gps_logic\n"
        )
        
        # Generate documentation for app.py
        self._create_file_if_not_exists(
            "docs/api/app.md",
            "# Application\n\n::: app\n"
        )
    
    def _generate_mkdocs_config(self) -> None:
        """Generate the mkdocs.yml configuration file."""
        import yaml
        
        # Update navigation based on existing files
        nav = []
        
        # Home page
        if (self.docs_dir / "docs" / "index.md").exists():
            nav.append({"Home": "index.md"})
        
        # API Reference
        api_pages = []
        if (self.docs_dir / "docs" / "api").exists():
            api_pages = self._get_api_pages()
        
        if api_pages:
            nav.append({"API Reference": api_pages})
        
        # Guides
        guide_pages = []
        if (self.docs_dir / "docs" / "guides").exists():
            guide_pages = self._get_guide_pages()
        
        if guide_pages:
            nav.append({"Guides": guide_pages})
        
        # Changelog
        if (self.docs_dir / "docs" / "changelog.md").exists():
            nav.append({"Changelog": "changelog.md"})
        
        # Update the config
        config = self.default_config.copy()
        config["nav"] = nav
        
        # Write the config file
        with open(self.mkdocs_config, "w", encoding="utf-8") as f:
            yaml.dump(config, f, sort_keys=False, allow_unicode=True)
        
        logger.info(f"Created mkdocs configuration at {self.mkdocs_config}")
    
    def _get_api_pages(self) -> List[Dict]:
        """Get a list of API documentation pages."""
        api_dir = self.docs_dir / "docs" / "api"
        pages = []
        
        for file in api_dir.glob("*.md"):
            if file.name != "index.md":
                name = file.stem.replace("_", " ").title()
                pages.append({name: f"api/{file.name}"})
        
        return pages
    
    def _get_guide_pages(self) -> List[str]:
        """Get a list of guide pages."""
        guide_dir = self.docs_dir / "docs" / "guides"
        pages = []
        
        for file in guide_dir.glob("*.md"):
            if file.name != "index.md":
                name = file.stem.replace("_", " ").title()
                pages.append({name: f"guides/{file.name}"})
        
        return pages
    
    def _create_file_if_not_exists(self, path: str, content: str) -> None:
        """Create a file with the given content if it doesn't exist."""
        file_path = self.docs_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.debug(f"Created file: {file_path}")
    
    @staticmethod
    def _get_index_content() -> str:
        """Get the content for the index page."""
        return """# Welcome to the GPS Application

## Overview

This is the documentation for the GPS Application built with Python and Streamlit.

## Features

- Interactive map display
- Marker management
- Route visualization
- Location tracking

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Documentation

- [Getting Started](guides/getting_started.md)
- [Development Workflow](guides/development_workflow.md)
- [API Reference](api/)
"""


def main():
    """Main entry point for the documentation generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate documentation for the project.")
    parser.add_argument(
        "--init",
        action="store_true",
        help="Initialize the documentation structure"
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Serve the documentation locally after generation"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to serve the documentation on (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to serve the documentation on (default: 8000)"
    )
    
    args = parser.parse_args()
    
    # Initialize the documentation generator
    generator = DocumentationGenerator()
    
    # Initialize documentation if requested
    if args.init:
        generator.initialize_docs()
    
    # Generate and optionally serve the documentation
    generator.generate_docs(serve=args.serve, strict=args.strict)


if __name__ == "__main__":
    main()
