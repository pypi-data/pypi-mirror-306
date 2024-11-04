from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'electf4_basicML',
    version = '0.1.7',
    packages = find_packages(),
    install_requires = [
    ],
    long_description = long_description,
    long_description_content_type = 'text/markdown'
)