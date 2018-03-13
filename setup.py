from setuptools import setup, find_packages

long_description = open('README.md').read()

setup(
    name='python-assignment',
    description='Python Assignment from Lei Wang',
    long_description = long_description,
    author='Lei Wang',
    author_email='wanglei.okay@gmail.com',
    keywords='stackexchange',
    install_requires=['requests'],
    version='0.1.0', 
    packages = find_packages(),
    package_data = {
        "":['*.md']
        },
    scripts = ["scripts/cli_stackOF.py"]


    )
