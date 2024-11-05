from setuptools import setup, find_packages

# Load README.md for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ebook2audiobook",
    version="0.0.4",  # or another version you choose
    author="Andrew Phillip Thomasson",
    author_email="drew.thomasson100@gmail.com",
    description="Convert eBooks to Audiobooks using TTS models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "coqui-tts==0.24.2",
        "pydub",
        "nltk",
        "beautifulsoup4",
        "ebooklib",
        "tqdm",
        "gradio==4.44.0"
    ],
    entry_points={
        'console_scripts': [
            'ebook2audiobookxtts=ebook2audiobook.launch:main',  # Launches `launch.py`'s main function
        ],
    },
    package_data={
        '': ['default_voice.wav'],
    },
    include_package_data=True,  # Ensures all specified files are included
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

