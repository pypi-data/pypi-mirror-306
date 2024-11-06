from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='video-aula-fiap-thiago-99',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib cursofiap',
    author='seu nome',
    author_email='thiagolazarin08@gmail.com',
    url='https://github.com/thiagolazarin/cursofiap.git',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
