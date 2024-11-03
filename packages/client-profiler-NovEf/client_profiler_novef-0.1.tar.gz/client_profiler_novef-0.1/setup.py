from setuptools import setup, find_packages

setup(
    name='client_profiler_NovEf',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'client_profiler_NovEf=client_profiler.__main__:main',
        ],
    },
    description='A package that will analyze customer'
                ' data and generate a detailed report.',
    author='Novoselov Efim',
    author_email='kuku@mail.com'
)