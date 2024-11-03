
from setuptools import setup, find_packages

setup(
    name='Tune_TEST010101',  # Replace with a unique name for PyPI
    version='1.0.0',      # Update version as needed
    author='Your Name',
    author_email='your.email@example.com',
    description='A sample project to showcase compilation and packaging',
    long_description='A more detailed description of the project.',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/Tune_TEST010101',  # Optional
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
