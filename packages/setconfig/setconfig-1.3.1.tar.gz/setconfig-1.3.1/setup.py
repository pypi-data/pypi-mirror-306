import re

from setuptools import setup, find_packages

REPO_NAME = 'setconfig'
PACKAGE_NAME = REPO_NAME.lower()
URL = f'https://github.com/abionics/{REPO_NAME}'


def get_version() -> str:
    code = read_file(f'{PACKAGE_NAME}/__init__.py')
    return re.search(r'__version__ = \'(.+?)\'', code).group(1)


def load_readme() -> str:
    return read_file('README.md')


def read_file(filename: str) -> str:
    with open(filename) as file:
        return file.read()


setup(
    name=PACKAGE_NAME,
    version=get_version(),
    description='Multi-structure YAML config loader 🐍🔌',
    long_description=load_readme(),
    long_description_content_type='text/markdown',
    author='Alex Ermolaev',
    author_email='abionics.dev@gmail.com',
    url=URL,
    license='MIT',
    keywords='config yaml dataclass pydantic init',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: System :: Installation/Setup',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Typing :: Typed',
    ],
    install_requires=[
        'pyyaml',
        'dacite',
        'pydantic',
    ],
    package_data={PACKAGE_NAME: ['py.typed']},
    packages=find_packages(exclude=['examples']),
    zip_safe=False,
)
