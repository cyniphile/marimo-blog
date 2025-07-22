# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a marimo-based blog that exports Python notebooks to static HTML pages. The project uses marimo for interactive notebooks and a custom build system to generate a static site.

## Architecture

- `apps/` - Contains marimo notebooks exported as applications (mode: run, code hidden)
- `notebooks/` - Contains marimo notebooks exported as editable notebooks (mode: edit)
- `public/` - Static assets (images, CSV data) accessible to notebooks
- `scripts/build.py` - Build script that exports all notebooks to HTML
- `_site/` - Generated static site output (created by build process)

## Development Commands

### Setup
```bash
# Install uv package manager
pip install uv

# Install dependencies
uv install
```

### Development
```bash
# Run marimo server with file watching
uv run marimo edit --watch
```

### Building and Testing
```bash
# Export all notebooks to static HTML
python scripts/build.py

# Serve the built site locally for testing
python -m http.server -d _site
# Site will be available at http://localhost:8000
```

## Notebook Structure

Notebooks should be placed in either:
- `apps/` - For standalone applications (exported without code visible)  
- `notebooks/` - For educational/tutorial notebooks (exported with code visible)

Data files and assets go in `public/` directory and can be accessed in notebooks using:
```python
mo.notebook_location() / "public" / "filename"
```

## Build Process

The build script (`scripts/build.py`):
1. Finds all `.py` files in `apps/` and `notebooks/` directories
2. Exports each using `marimo export html-wasm`
3. Apps are exported with `--mode run --no-show-code`
4. Notebooks are exported with `--mode edit`
5. Generates an index.html file listing all notebooks