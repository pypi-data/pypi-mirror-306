from setuptools import setup

setup(
    name='list_utilities',  
    version='0.1.1',  
    author='Navdeep singh, Group 4',  
    author_email='160320243@ggi.ac.in',  
    description='A Python package for common list operations such as removing duplicates and flattening lists.',
    long_description=open('README.md').read(),  # Read from README.md for detailed description
    long_description_content_type='text/markdown',  # Specify markdown format for PyPI

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',   
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
