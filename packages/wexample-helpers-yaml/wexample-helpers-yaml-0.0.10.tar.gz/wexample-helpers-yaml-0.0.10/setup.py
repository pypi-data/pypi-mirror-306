from setuptools import setup, find_packages

setup(
    name='wexample-helpers-yaml',
    version=open('version.txt').read(),
    author='weeger',
    author_email='contact@wexample.com',
    description='Helpers for reading yaml files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wexample/python-helpers-yaml',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pyyaml',
        'pydantic',
        'wexample-helpers',
    ],
    python_requires='>=3.6',
)
