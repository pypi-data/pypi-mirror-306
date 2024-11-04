from setuptools import setup, find_packages

setup(
    name="nova-client-sdk",
    version="0.1.0",
    author="ScottyLabs",
    author_email="hello@scottylabs.org",
    description="A Python client SDK for the Nova hackathon",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ScottyLabs/nova-python-sdk",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
