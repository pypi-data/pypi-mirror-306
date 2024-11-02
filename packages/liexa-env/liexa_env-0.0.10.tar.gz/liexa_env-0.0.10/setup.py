from setuptools import setup, find_packages

setup(
    name="liexa-env",
    version="0.0.10",
    description="A Python package for environment management.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="lifedrivendev",
    author_email="lifedrivendeveloper@gmail.com",
    url="https://github.com/lifedrivendev/liexa-env",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
