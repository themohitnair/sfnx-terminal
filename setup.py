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
    python_requires='>=3.7',  # Specify Python version requirements
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
