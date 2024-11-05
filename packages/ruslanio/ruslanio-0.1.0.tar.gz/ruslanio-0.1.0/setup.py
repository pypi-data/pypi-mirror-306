from setuptools import setup
import os.path


PACKAGE_NAME = 'ruslanio'


def get_full_path(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, rel_path)


def read(rel_path):
    with open(get_full_path(rel_path), 'r') as f:
        return f.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1].strip()
    else:
        raise RuntimeError("Unable to find version string.")

def get_packages(rel_path):
    path = get_full_path(rel_path)
    result = []
    if os.path.isdir(path):
        names = os.listdir(path)
        if '__init__.py' in names:
            result.append(rel_path)
        for name in names:
            new_path = os.path.join(rel_path, name)
            result.extend(get_packages(new_path))
    return result


setup(
    name=PACKAGE_NAME,
    version=get_version(f'{PACKAGE_NAME}/__init__.py'),
    description='My personal tools for my projects',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Ruslan Baynazarov',
    author_email='',
    url='https://github.com/hocop/ruslanio',
    packages=get_packages(PACKAGE_NAME),
    license="WTFPL",
    include_package_data=True,
    install_requires=read('requirements.txt').splitlines()
)
