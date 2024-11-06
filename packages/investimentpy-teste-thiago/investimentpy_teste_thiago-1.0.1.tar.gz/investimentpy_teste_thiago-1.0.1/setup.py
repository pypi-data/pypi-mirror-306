from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='investimentpy_teste_thiago',
    version='1.0.1',
    packages=find_packages(),
    description='Uma biblioteca para análise de investimentos',
    author='Thiago R L',
    author_email='thiagolazarin08@gmail.com',
    url='https://github.com/tadrianonet/investimentpy',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown' 
)