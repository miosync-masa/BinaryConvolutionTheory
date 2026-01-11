"""
Binary Convolution Theory (BCT) - Setup
"""

from setuptools import setup, find_packages

setup(
    name="bct",
    version="1.0.0",
    description="Binary Convolution Theory: A Structural Approach to Perfect Numbers",
    author="Masamichi Iizumi, Tamaki Iizumi",
    author_email="m.iizumi@miosync.email",
    url="https://github.com/miosync-masa/BinaryConvolutionTheory",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
