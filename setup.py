from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='rUtils',
    version='0.0.7',
    description='my general tools',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Sergio Cricca',
    author_email='sergio.cricca@gmail.com',
    keywords=['rUtils', 'utils', 'scheduler', 'elastic', 'splauto'],
    url='https://github.com/riogezz/myPyClass',
    download_url=''
)

install_requires = [
    'schedule',
    'munch',
    'PyYAML',
    'elasticsearch',
    'retrying',
    'selenium',
    'splinter'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)