from setuptools import setup

# Lendo as dependências do arquivo requirements.txt
with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()
    requirements = [line.strip() for line in requirements if line.strip() and not line.startswith("#")]

setup(
    name='AutoReg-Mrpac6689',
    version='4.2.4',
    py_modules=['autoreg4'],  # py_modules é usado para módulos na raiz do projeto
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'autoreg=autoreg4:criar_janela_principal'  # Nome do comando para execução do programa
        ]
    },
    author='Michel Ribeiro Paes',
    description='AUTOREG - Operação automatizada de Sistemas - SISREG & G-HOSP',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/seu_usuario/seu_repositorio',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
