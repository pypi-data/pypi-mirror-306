# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'gentle'
author = 'Anna <cyber@sysrq.in>'
copyright = f'2022-2024, {author}'
release = '1.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx_prompt',
]

try:
    import notfound.extension
    extensions.append('notfound.extension')

    notfound_urls_prefix = None
except ModuleNotFoundError:
    pass

try:
    import sphinx_sitemap
    extensions.append('sphinx_sitemap')

    sitemap_locales = [None]
    sitemap_url_scheme = '{link}'
    sitemap_excludes = [
        '404.html',
    ]
except ModuleNotFoundError:
    pass

root_doc = 'toc'
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
manpages_url = 'https://docs.sysrq.in/{path}'

extlinks = {
    'bug': ('https://bugs.sysrq.in/show_bug.cgi?id=%s', 'bug #%s'),
    'gentoobug': ('https://bugs.gentoo.org/%s', 'Gentoo bug #%s'),
    'gitweb': (f'https://git.sysrq.in/{project}/tree/%s', '%s'),
    'pypi': ('https://pypi.org/project/%s/', '%s'),
}
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
}

autosummary_generate = False
autodoc_default_options = {
    'show-inheritance': True,
    'undoc-members': True,
    'member-order': 'bysource',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'insipid'
html_permalinks_icon = '#'
html_theme_options = {
    'globaltoc_maxdepth': 3,
    'right_buttons': ['git-button.html'],
}
html_sidebars = {
    '**': [
        'globaltoc.html',
    ]
}
html_context = {
    'git_repo_url': 'https://git.sysrq.in/gentle/about/',
}

html_static_path = ['_static']
html_title = f'{project} {release}'
html_baseurl = 'https://gentle.sysrq.in/'
