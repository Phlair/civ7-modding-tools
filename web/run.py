#!/usr/bin/env python3
"""
Quick script to run the Civ VII Mod Editor web server.

Usage:
    python web/run.py
    # OR from project root:
    uv run python web/run.py
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


if __name__ == "__main__":
    try:
        import uvicorn

        print(
            """
    ╔═══════════════════════════════════════════════════════════════╗
    ║          Civ VII Mod Editor - Web Server                      ║
    ║                                                               ║
    ║  🌐 Server: http://127.0.0.1:8000                            ║
    ║  📚 API Docs: http://127.0.0.1:8000/docs                     ║
    ║  🛑 Press Ctrl+C to stop                                      ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
        )

        uvicorn.run(
            "web.app:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info",
        )

    except ImportError as e:
        print(
            f"Error: Required dependencies not installed.\n{e}\n"
            "Please run: uv sync --extra web\n"
            "Or: pip install -e '.[web]'"
        )
        sys.exit(1)
