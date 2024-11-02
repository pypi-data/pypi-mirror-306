from setuptools import setup, find_packages

setup(
    name="pyladdersim",
    version="0.1.0",
    author="Akshat Nerella",
    author_email="akshatnerella27@gmail.com",
    description="An educational ladder logic simulator in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/akshatnerella/pyladdersim",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
