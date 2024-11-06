from setuptools import setup, find_packages

setup(
    name='Y_lw',  # Package name
    version='0.2.1',  # Initial version
    packages=find_packages(),  # Automatically find packages
    description='A simple library that prints a greeting.',
    long_description=open('README.md').read(),  # Long description from README
    long_description_content_type='text/markdown',
    author='Y-ellow',  # Replace with your name
    author_email='im.yellow.dev@gmail.com',  # Replace with your email
    url='https://github.com/im-yellow/Y_ellow/',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
)
