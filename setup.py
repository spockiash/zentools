from setuptools import setup, find_packages

setup(
    name="zentools",
    version="0.1.1",
    description="A library for algorithmic analysis using Pandas and NumPy",
    author="Bobo",
    author_email="theb02b04@gmail.com",
    license="MIT",
    packages=find_packages(),  # Automatically discovers submodules
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
