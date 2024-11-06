from setuptools import setup, find_packages

setup(
    name="simp_sql",
    version="0.1.2",
    author="Nikhil Kumawat",
    description="A package that generates and optimizes SQL queries.",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python>=8.0.0"  # List your dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)