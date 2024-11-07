from setuptools import setup, find_packages

setup(
    name="gate-manager",
    version="1.0.3",
    author="Chen Huang",
    author_email="chen.huang23@imperial.ac.uk",
    description="A package for interfacing with the Nanonis system for voltage control and data acquisition.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chenx820/gate-manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "matplotlib>=3.0",
        "tqdm>=4.0",
        "nanonis_tramea>=1.0"
    ],
)
