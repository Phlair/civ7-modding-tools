"""
Civ VII Mod Editor Web Interface

A beautiful, intuitive web UI for editing Civilization VII mod YAML files.
Built with FastAPI, HTMX, and Tailwind CSS.

Usage:
    python web/run.py
    # OR
    uv run python web/run.py

Then open: http://127.0.0.1:8000
"""

__version__ = "1.0.0"
__all__ = ["app"]

from web.app import app

__doc__ = """
Civ VII Mod Editor Web Interface

Fast-reload development server:
    uvicorn web.app:app --reload --host 127.0.0.1 --port 8000

Production server:
    uvicorn web.app:app --host 0.0.0.0 --port 8000

API Documentation:
    http://127.0.0.1:8000/docs (Swagger UI)
    http://127.0.0.1:8000/redoc (ReDoc)
"""
