from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="OptionsPricerLib",
    version="0.1.1",
    description="A library for pricing options using different models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="hedge0",
    url="https://github.com/hedge0/OptionsPricerLib",
    packages=find_packages(),
    install_requires=["numpy", "numba"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
