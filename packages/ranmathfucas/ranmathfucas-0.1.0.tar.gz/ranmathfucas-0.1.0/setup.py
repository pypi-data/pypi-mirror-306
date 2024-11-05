from setuptools import setup, find_packages

setup(
    name="ranmathfucas",
    version="0.1.0",
    packages=find_packages(),
    description="A simple math library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Harish",
    author_email="harish00411@gmail.com",
    url="https://github.com/yourusername/ranmathfucas", # URL for the library’s GitHub
    license="MIT",                            # License type
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)