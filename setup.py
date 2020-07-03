from setuptools import setup, find_packages

setup(
    name="crossword_downloader",
    version="0.1",
    description="Download NYT crossword puzzles.",
    url="http://github.com/benshanahan1/crossword_downloader",
    packages=find_packages(),
    install_requires=["requests", "python-dateutil"],
    extras_require={"dev": ["flake8", "pytest", "pytest-pep8", "pytest-cov"]},
    entry_points="""
        [console_scripts]
        crossword_downloader=src.__init__:main
    """,
)
