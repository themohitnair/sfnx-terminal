from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sfnx",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "typer[all]>=0.4,<1.0",
        "rich>=10.0,<13.0",
        "cryptography>=3.4,<41.0",
        "argon2-cffi>=20.1,<23.0",
        "sqlmodel>=0.0.4,<0.1.0",
        "pyperclip>=1.9.0"
    ],
    entry_points={
        "console_scripts": [
            "sfnx=sfnx.main:app",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
)