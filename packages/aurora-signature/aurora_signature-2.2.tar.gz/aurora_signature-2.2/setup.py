from setuptools import setup, find_packages

setup(
    name="aurora_signature",
    version="2.2",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "aurora = aurora_signature:cli"
        ]
    }
)