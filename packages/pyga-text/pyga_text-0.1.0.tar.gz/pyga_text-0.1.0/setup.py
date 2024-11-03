from setuptools import setup, find_packages

setup(
    name='pyga-text',  # Nome do seu pacote
    version='0.1.0',  # Versão do seu pacote
    packages=find_packages(),  # Encontra todos os pacotes
    install_requires=[],  # Dependências, se houver
    description='Uma biblioteca para manipulação de textos e personagens em Python',
    long_description=open('README.md').read(),  # Conteúdo do README
    long_description_content_type='text/markdown',  # Tipo do conteúdo
    author='Joao',  # Substitua pelo seu nome
    author_email='jpg01153@gmail.com',  # Substitua pelo seu e-mail
    license='MIT',  # Licença
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versão mínima do Python
)