from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='pyargv',
    version='0.1.0',
    description='argument load from command line',
    long_description=readme,
    author='Arthur Lu',
    author_email='asirlu@foxmail.com',
    url='https://github.com/lsj9383/pyargv',
    # license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)