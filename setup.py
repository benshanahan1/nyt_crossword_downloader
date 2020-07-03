from setuptools import setup, find_packages

setup(
    name="nyt_crossword_downloader",
    version="0.1",
    description="Download NYT crossword puzzles.",
    url="http://github.com/benshanahan1/nyt_crossword_downloader",
    packages=find_packages(),
    install_requires=["requests", "python-dateutil"],
    extras_require={"dev": ["black", "flake8", "pytest", "pytest-pep8", "pytest-cov"]},
    entry_points="""
        [console_scripts]
        nyt_crossword_downloader=nyt_crossword_downloader.__init__:main
    """,
)
