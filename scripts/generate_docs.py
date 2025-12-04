"""
Generate static API documentation using pdoc.

This sets up Django so modules that rely on settings/apps can import cleanly.
Outputs HTML under docs/.
"""

import os
from pathlib import Path

import django
from pdoc import pdoc


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    os.environ.setdefault("PYTHONPATH", str(project_root))

    django.setup()
    output_dir = project_root / "docs"
    pdoc(
        "trips",
        "ml_models",
        output_directory=output_dir,
    )


if __name__ == "__main__":
    main()
