# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pygbm'
copyright = '2024, Dario Zela'
author = 'Dario Zela'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.duration",
            "sphinx.ext.autodoc",
            "sphinx.ext.autosummary",
            "sphinx_rtd_theme",
            "m2r2"]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

# Add your module's path to `sys.path`
import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # Point to your project source code

# Get the current directory
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")