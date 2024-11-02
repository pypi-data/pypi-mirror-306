# setup.py

from setuptools import setup, find_packages

setup(
    name="flipkart_miraie_ac",  # The name of your package on PyPI
    version="0.0.1",
    author="Pratik Bhoir",
    author_email="pratbhoir@gmail.com",
    description = "Flipkart-MirAIe-AC API for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
