
# 🗺️ GPS Application with Vibe Coding

Welcome to the GPS Application, a Python-based tool for managing and visualizing geographic locations with markers on an interactive map. This project follows the Vibe Coding methodology with automated testing, documentation, and continuous integration.

## 🌟 Features

- **Interactive Map**: Visualize locations using Folium maps with custom markers
- **Marker Management**: Add, save, and manage points of interest
- **Real-time Location**: Get your current location via IP geolocation
- **Vibe Coding Workflow**: Automated development workflow with AI assistance
- **Comprehensive Testing**: Unit and integration tests with high coverage
- **Automated Documentation**: Self-updating API documentation

## 🛠️ Requirements

- Python 3.10+
- Git
- pip (Python package manager)

## 🚀 Quick Start

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/gps-application.git
   cd gps-application
   ```

2. **Set up a virtual environment**:

   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Linux/MacOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Run the application**:

   ```bash
   streamlit run app.py
   ```
   The application will open in your default web browser.

## 🧪 Testing

Run the test suite with pytest:

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest --cov=. --cov-report=html
```

## 📚 Documentation

### Generating Documentation

Documentation is automatically generated from docstrings using mkdocs. To generate and serve the documentation locally:

```bash
# Install documentation dependencies
pip install -r requirements-dev.txt

# Generate and serve documentation
python scripts/generate_docs.py --serve
```

### Vibe Coding Workflow

This project follows the Vibe Coding methodology, which includes:

- **Automated Testing**: Continuous testing with pytest
- **Code Quality**: Pre-commit hooks for code formatting and linting
- **Documentation**: Auto-generated from docstrings
- **CI/CD**: GitHub Actions for continuous integration

## 🤖 AI-Assisted Development

This project includes AI-assisted development tools:

- `scripts/generate_tests.py`: Automatically generates test cases for your code
- `scripts/generate_docs.py`: Generates documentation from docstrings
- `.windsurf/`: Contains configuration for Vibe Coding workflow

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the web interface
- [Folium](https://python-visualization.github.io/folium/) for interactive maps
- [Pytest](https://docs.pytest.org/) for testing
- [MkDocs](https://www.mkdocs.org/) for documentation
