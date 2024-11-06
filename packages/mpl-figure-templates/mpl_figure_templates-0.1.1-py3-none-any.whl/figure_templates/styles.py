"""
Define styles of figures.
"""

import matplotlib.pyplot as plt
import matplotlib.style

from .config import find_config_directories


def style(*args):
    """
    Get a context manager for figure styles
    """
    return plt.style.context(*args)


def reload_styles():
    """
    Load local and matplotlib stylesheets
    """
    # Erase and reload standard matplotlib styles
    matplotlib.style.reload_library()

    # Load stylesheets in all our local configuration directories
    stylesheet_dirs = find_config_directories("stylesheets")
    for path in stylesheet_dirs:
        styles = matplotlib.style.core.read_style_directory(path)  # type: ignore
        matplotlib.style.library.update(styles)

    matplotlib.style.available[:] = sorted(matplotlib.style.library.keys())


reload_styles()
