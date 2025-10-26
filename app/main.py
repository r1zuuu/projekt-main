"""Application entry point for running the Flask development server."""
from __future__ import annotations

from . import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
