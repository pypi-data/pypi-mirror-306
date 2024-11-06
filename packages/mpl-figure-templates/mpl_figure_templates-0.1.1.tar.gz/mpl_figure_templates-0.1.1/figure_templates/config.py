"""
Manage the configuration of the project.
"""

import os
from pathlib import Path
from typing import Literal

import platformdirs
from dotenv import load_dotenv


def find_config_directories(name: Literal["stylesheets", "layouts"]) -> list[Path]:
    """
    Find all configuration directories for the given configuration name.

    The directories are searched in the following order:

    - the package directory (which contains `layouts` and `stylesheets` directories),
    - the `mpl_figure_templates` directory in the platform-dependent user configuration
      directory,
    - by default, the `figure_templates` directory in the current working directory.
      This directory can be changed by setting the `MPL_FIGURE_TEMPLATES_CONFIG_DIR`
      environment variable.

    Only existing directories are returned.
    """
    if name not in ["stylesheets", "layouts"]:
        raise ValueError(f"Invalid config name: {name}")

    APP_NAME = "mpl_figure_templates"
    config_dirs = [
        Path(__file__).parent / name,
        Path(platformdirs.user_config_dir(APP_NAME)) / name,
    ]
    # Add the local configuration directory, possibly set by environment variable
    load_dotenv()
    additional_config_dir = os.getenv("MPL_FIGURE_TEMPLATES_CONFIG_DIR")
    if additional_config_dir is not None:
        config_dirs.append(Path(additional_config_dir) / name)
    else:
        config_dirs.append(Path() / "figure_templates" / name)

    return [d for d in config_dirs if d.exists()]
