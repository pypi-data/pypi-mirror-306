from setuptools import setup, find_packages

setup(
    name="find-in-pdf",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "PyPDF2>=3.0.0",
    ],
    entry_points={
        'console_scripts': [
            'pdfsearcher=pdfsearcher.search:main',
        ],
    },
    author="Ognjen Lazic",
    author_email="laogdo@gmail.com",
    description="A simple tool to search for strings in PDF files within a directory.",
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
