from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import shutil

class PostInstallCommand(install):
    def run(self):
        # Run the original install process
        install.run(self)
        
        # Import nltk only after dependencies are installed
        import nltk
        # Post-install NLTK download
        nltk.download("punkt")
        nltk.download("punkt_tab")
        
        # Ensure default_voice.wav is available for app.py
        default_voice_src = os.path.join(os.path.dirname(__file__), 'default_voice.wav')
        default_voice_dest = os.path.join(os.path.expanduser("~"), '.ebook2audiobook', 'default_voice.wav')
        os.makedirs(os.path.dirname(default_voice_dest), exist_ok=True)
        shutil.copyfile(default_voice_src, default_voice_dest)

setup(
    name="ebook2audiobook",
    version="0.0.1",
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
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'ebook2audiobook=your_package.app:main',
        ],
    },
    package_data={
        '': ['default_voice.wav'],
    },
)

