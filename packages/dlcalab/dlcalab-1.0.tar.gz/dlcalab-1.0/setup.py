from setuptools import setup, find_packages

setup(
    name='dlcalab',
    version='1.0',
    packages=find_packages(),
    install_requires=[],
    package_data={'dlcalab': ['*.txt', '*.html', '*.zip', '*.jpg']},
)
