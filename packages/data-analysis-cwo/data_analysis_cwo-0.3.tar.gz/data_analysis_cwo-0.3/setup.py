from setuptools import setup, find_packages

setup(
    name='data-analysis-cwo',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'time',
        'pandas',
        'matplotlib',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'data-analysis-cwo=src.main:main',
        ],
    },
    description='A data-analysis tool for cwo project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Shashikant Pathak',
    author_email='s.pathak@ugent.be',
    url='https://github.com/shashikantpathakk3/data-analysis',
)