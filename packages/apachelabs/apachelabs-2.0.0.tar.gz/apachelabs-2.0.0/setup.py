# setup.py

from setuptools import setup, find_packages

setup(
    name="apachelabs",
    version="2.0.0",
    packages=find_packages(),
    install_requires=["mistralai"],  # This is required for the Mistral API
    author="Apache Labs",
    author_email="your.email@example.com",
    description="Apache Labs API is a Python package that uses Mistral and Hugging Face to create a simple and unified API system to use all of the Apache Labs models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/apachelabs",  # Replace with your repo link
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
