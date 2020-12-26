import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CyPerAna",
    version="0.0.0.dev",
    author="Stefano Vanin",
    description="CYcling PERformance ANAlyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stefano-v37/cyperana",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)