from setuptools import setup, find_packages

library_description = ""
with open('README.md', 'r', encoding="utf-8") as f:
    library_description = f.read()

setup(
    name='csecraft',
    version='0.1.1',
    description='A Python library for easily interacting with the Google Custom Search API',
    long_description=library_description,
    long_description_content_type='text/markdown',
    author='Benard K. Wachira (@benkimz)',
    maintainer='@benkimz',
    url='https://github.com/benkimz/cse-api',
    license='MIT',
    keywords=['google', 'cse', 'api', 'search', 'custom search'],
    platforms=['any'],
    packages=find_packages(),
    install_requires=[
        # Dependencies
        'requests',
        'pydantic',
        'typing'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)