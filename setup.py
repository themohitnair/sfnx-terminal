from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sfnx",
    version="0.2.2",
    packages=find_packages(),
    install_requires=[
        "typer[all]>=0.9.0,<1.0",
        "rich>=13.6.0,<14.0",
        "cryptography>=41.0.4,<42.0",
        "argon2-cffi>=23.1.0,<24.0",
        "sqlmodel>=0.0.11,<0.1.0",
        "pyperclip>=1.8.2,<2.0"
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