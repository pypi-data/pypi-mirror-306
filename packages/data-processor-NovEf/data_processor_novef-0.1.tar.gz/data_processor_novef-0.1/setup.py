from setuptools import setup, find_packages

setup(
    name='data-NovEf-processor',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'data-NovEf-processor=data_processor.__main__:main',
        ],
    },
    description='A package that will automatically'
                ' download sales data, analyze it and generate '
                'a report in the form of a CSV file.',
    author='Novoselov Efim',
    author_email='kuku@mail.com'
)