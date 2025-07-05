# Scripts Directory

This directory contains automation scripts that support the Vibe Coding workflow for the GPS application.

## Available Scripts

### `generate_tests.py`

Automatically generates test cases for Python modules using static analysis.

**Usage:**
```bash
python scripts/generate_tests.py path/to/module.py
```

**Options:**
- `--output-dir`: Directory to save generated test files (default: `tests/`)
- `--template`: Path to a custom test template file
- `--verbose`: Enable verbose output
- `--dry-run`: Show what would be generated without writing files

### `generate_docs.py`

Generates project documentation from docstrings using MkDocs and mkdocstrings.

**Usage:**
```bash
# Generate and serve documentation
python scripts/generate_docs.py --serve

# Just generate docs without serving
python scripts/generate_docs.py
```

**Options:**
- `--serve`: Start a local server to preview the documentation
- `--port`: Port to serve documentation on (default: 8000)
- `--clean`: Remove existing build directory before generating

### `vibe_coder.py`

Main script for AI-assisted development following the Vibe Coding methodology.

**Usage:**
```bash
python scripts/vibe_coder.py [command] [options]
```

**Commands:**
- `generate-tests`: Generate test cases for a module
- `generate-docs`: Generate project documentation
- `run-workflow`: Run the complete Vibe Coding workflow

## Development

### Adding New Scripts

1. Create a new Python file in this directory
2. Add a command-line interface using `argparse`
3. Include comprehensive error handling and logging
4. Add a section to this README documenting the script's purpose and usage

### Best Practices

- Use the `logging` module for output
- Include type hints for better code clarity
- Add docstrings following Google style guide
- Write tests for your scripts in the `tests/` directory
- Keep scripts focused on a single responsibility

## Dependencies

All scripts should list their dependencies in `requirements-dev.txt` and check for them at runtime.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
