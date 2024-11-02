from setuptools import setup, find_packages

setup(
    name='receipt_generator_NovEf',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'receipt_generator_NovEf=receipt_generator.__main__:main',
        ],
    },
    description='A package that will automatically generate '
                'a receipt based on the order information and'
                ' save it in a text file.',
    author='Novoselov Efim',
    author_email='kuku@mail.com'
)