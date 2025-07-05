"""
Simple Vibe Coding Setup for GPS Application
"""
import os
from pathlib import Path

def create_directories():
    """Create necessary directories."""
    dirs = [
        "scripts",
        "tests/unit",
        "tests/integration",
        "docs",
        ".github/workflows"
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_requirements():
    """Create requirements files."""
    # Main requirements
    requirements = [
        "streamlit>=1.22.0",
        "folium>=0.14.0",
        "geocoder>=1.38.1",
        "streamlit-folium>=0.15.1",
        "pytest>=7.3.1",
        "black>=23.3.0",
        "flake8>=6.0.0",
        "mypy>=1.0.0",
        "pre-commit>=3.2.0"
    ]
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(requirements))
    
    print("Created requirements.txt")

def create_github_workflow():
    """Create GitHub Actions workflow."""
    workflow = """name: Vibe Coding

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest tests/ -v
    - name: Check code style
      run: |
        black --check .
        flake8 .
"""
    os.makedirs('.github/workflows', exist_ok=True)
    with open('.github/workflows/vibe.yml', 'w', encoding='utf-8') as f:
        f.write(workflow)
    print("Created GitHub workflow")

def main():
    """Main setup function."""
    print("Setting up Vibe Coding...")
    create_directories()
    create_requirements()
    create_github_workflow()
    print("\nSetup complete! Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Initialize git: git init")
    print("3. Add files: git add .")
    print("4. Commit: git commit -m 'Initial commit'")
    print("5. Run the app: streamlit run app.py")

if __name__ == "__main__":
    main()
