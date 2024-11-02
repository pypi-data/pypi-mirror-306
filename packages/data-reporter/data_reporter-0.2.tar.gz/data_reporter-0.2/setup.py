from setuptools import setup, find_packages

setup(
    name='data-reporter-NovEf',
    version='0.2',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'data-reporter-NovEf=data_reporter.__main__:main',
        ],
    },
    description='A package for calculating which will download transaction data, '
                'group them by categories (income and expenses) and generate a '
                'report with amounts for each category.',
    author='Novoselov Efim',
    author_email='kuku@mail.com'
)