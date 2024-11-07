from setuptools import setup, find_packages

setup(
    name='wexample-prompt',
    version=open('version.txt').read(),
    author='weeger',
    author_email='contact@wexample.com',
    description='Helper for your tty interactions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wexample/python-prompt',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pydantic',
        'rich',
    ],
    python_requires='>=3.6',
)
