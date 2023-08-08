#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sphinx configuration."""
# Imports #
# Standard Libraries #
from datetime import datetime

# Third-Party Packages #

# Local Packages #


# Definitions #
project = "base objects"
author = "Anthony Fong"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "sphinx_rtd_theme",
]
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"
