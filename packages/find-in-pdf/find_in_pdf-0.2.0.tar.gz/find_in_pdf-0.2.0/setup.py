from setuptools import setup, find_packages

setup(
    name="find-in-pdf",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "pdfplumber>=0.11.4",
    ],
    entry_points={
        'console_scripts': [
            'pdfutil=pdfsearcher.search:main',  # Single command for both modes
        ],
    },
    author="Ognjen Lazic",
    author_email="laogdo@gmail.com",
    description="A simple tool to search for strings or list PDF files within a directory.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anitejngo/pdfsearcher",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
