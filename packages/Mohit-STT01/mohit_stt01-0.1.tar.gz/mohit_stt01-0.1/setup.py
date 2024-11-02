from setuptools import setup, find_packages
import os


long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name='Mohit_STT01',
    version='0.1',
    author='Mohit Kumar',
    author_email='megamohit2006@gmail.com',
    description='This is a speech-to-text package created by Mohit Kumar',
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional, if using Markdown for README
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver_manager'
    ],
    include_package_data=True,
    package_data={
        'Mohit_SpeechToText': ['index.html', 'script.js', 'style.css', 'input.txt'],  # Include all necessary files
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
