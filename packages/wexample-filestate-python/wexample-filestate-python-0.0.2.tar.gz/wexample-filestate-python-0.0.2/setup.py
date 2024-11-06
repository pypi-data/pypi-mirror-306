from setuptools import setup, find_packages

setup(
    name='wexample-filestate-python',
    version=open('version.txt').read(),
    author='weeger',
    author_email='contact@wexample.com',
    description='Helpers for Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wexample/python-filestate-python',
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
    ],
    python_requires='>=3.6',
)
