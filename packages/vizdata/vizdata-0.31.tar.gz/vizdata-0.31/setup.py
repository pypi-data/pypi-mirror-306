from setuptools import setup

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="vizdata",
    version="0.31",
    description="Simple Exploratory Data Analysis tool.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/darkhan-ai/vizdata",
    license="MIT",
    packages=["vizdata"],
    install_requires=[
        "pandas",
    ],
    zip_safe=False,
)
