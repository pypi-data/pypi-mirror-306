# setup.py
from setuptools import setup, find_packages


with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="quantics",
    version="0.2.0",
    author="Daniel Igbokwe",
    author_email="igbodani14@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "umap-learn",
        "numpy",
        "pandas",
        "scikit-learn"
    ],

)
