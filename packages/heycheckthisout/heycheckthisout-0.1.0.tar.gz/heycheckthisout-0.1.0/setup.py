# setup.py
from setuptools import setup, find_packages

setup(
    name="heycheckthisout",                # Package name
    version="0.1.0",                  # Version
    author="Your Name",               # Author name
    author_email="your.email@example.com",  # Author email
    description="A simple example package", # Short description
    long_description=open("README.md").read(), # Long description (from README)
    long_description_content_type="text/markdown", # Content type
    url="https://github.com/yourusername/my_package", # Project URL
    packages=find_packages(),         # Finds all packages within the directory
    classifiers=[                     # Classifiers to categorize the package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",          # Python version requirements
)
