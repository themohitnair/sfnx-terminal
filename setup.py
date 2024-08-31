from setuptools import setup, find_packages

setup(
    name="sfnx",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich",
        "cryptography",
        "argon2-cffi",
        "sqlmodel"
    ],
    entry_points={
        "console_scripts": [
            "sfnx=sfnx.main:app",
        ],
    },
)
