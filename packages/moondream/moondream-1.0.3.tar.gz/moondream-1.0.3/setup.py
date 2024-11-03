from setuptools import setup, find_packages
from pathlib import Path

# read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="moondream",
    version="1.0.3",
    packages=find_packages(include=['moondream', 'moondream.*']),
    install_requires=[
        "torch",
        "Pillow",
        "transformers",
    ],
    entry_points={
        'console_scripts': [
            'moondream=moondream.torch.inference:main',
        ],
    },
    author="1997marsrover",
    author_email="antonygithinji11156@gmail.com",
    description="A package for image-based question answering using Moondream",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1997MarsRover/moondream",
    project_urls={
        'Bug Tracker': 'https://github.com/1997MarsRover/moondream/issues',
        'Documentation': 'https://github.com/1997MarsRover/moondream#readme',
        'Source Code': 'https://github.com/1997MarsRover/moondream',
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",  # Updated for 1.0+ version
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
)