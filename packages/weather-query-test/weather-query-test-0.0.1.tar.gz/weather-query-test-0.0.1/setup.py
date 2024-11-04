from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="weather-query-test",
    version="0.0.1",
    author="Wook Lee",
    author_email="leewook94@gmail.com",
    description="forecast weather",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["api", "weather", "forecast"],
    packages=find_packages(),
    install_requires=[
        "googletrans==4.0.0rc1",
        "python-dotenv>=1.0.1",
        "python-multipart>=0.0.12",
        "requests>=2.32.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
