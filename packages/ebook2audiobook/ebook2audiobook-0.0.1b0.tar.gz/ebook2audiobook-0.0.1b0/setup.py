from setuptools import setup, find_packages

setup(
    name="ebook2audiobook",
    version="0.0.1b",
    author="Andrew Phillip Thomasson",
    author_email="drew.thomasson100@gmail.com",
    description="A package to convert ebooks to audiobooks",
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
            'ebook2audiobook=your_package.app:main',
        ],
    },
    package_data={
        '': ['default_voice.wav'],
    },
)

