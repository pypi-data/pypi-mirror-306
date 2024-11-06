from setuptools import setup, find_packages

setup(
    name='cwo_analysis',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'cwo_analysis=data_analysis_cwo.main:run',
        ],
    },
    description='A data-analysis tool for cwo project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Shashikant Pathak',
    author_email='s.pathak@ugent.be',
    url='https://github.com/shashikantpathakk3/data-analysis',
)


