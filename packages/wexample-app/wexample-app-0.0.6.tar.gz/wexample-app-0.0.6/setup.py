from setuptools import setup, find_packages

setup(
    name='wexample-app',
    version=open('version.txt').read(),
    author='weeger',
    author_email='contact@wexample.com',
    description='Helpers for building Python app or cli.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wexample/python-app',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'python-dotenv',
        'pydantic',
        'wexample-filestate',
        'wexample-helpers',
        'wexample-prompt',
    ],
    python_requires='>=3.6',
)
