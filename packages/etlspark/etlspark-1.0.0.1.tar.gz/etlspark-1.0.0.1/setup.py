from setuptools import setup, find_packages

setup(
    name="etlspark",
    version="1.0.0.1",
    packages=find_packages(),
    install_requires=[],
    description="Lib etl",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jonathan",
    author_email="jonathan-works@hotmail.com",
    url="https://github.com/jonathan-works/etlbr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
